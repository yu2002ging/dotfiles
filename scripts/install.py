#!/usr/bin/env python3
"""Link managed configurations, keeping a reversible journal outside the repo."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
LINKS = {
    'zsh/.zshrc': '.zshrc',
    'zsh/.zprofile': '.zprofile',
    'zsh/terminal.zsh': '.config/zsh/terminal.zsh',
    'nvim': '.config/nvim',
    'wezterm/wezterm.lua': '.config/wezterm/wezterm.lua',
    'starship/starship.toml': '.config/starship.toml',
}
PRIVATE = re.compile(r'^\s*export (?:ANTHROPIC_API_KEY|ANTHROPIC_BASE_URL|HTTP_PROXY|HTTPS_PROXY|ALL_PROXY|http_proxy|https_proxy|all_proxy)=.*$', re.M)

def exists(p):
    return os.path.lexists(p)

def correct(p, source):
    return p.is_symlink() and p.resolve() == source.resolve()

def save(journal, data):
    temp = journal.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n')
    temp.chmod(0o600)
    temp.replace(journal)

def rollback(journal, dry=False):
    data = json.loads(journal.read_text())
    # Verify everything before changing anything. Never overwrite later user files.
    for entry in reversed(data['entries']):
        p = Path(entry['target'])
        if entry['kind'] == 'link':
            if exists(p) and not (p.is_symlink() and os.readlink(p) == entry['source']):
                raise RuntimeError(f'Rollback conflict (file changed): {p}')
            backup = Path(entry['backup']) if entry.get('backup') else None
            if backup and not exists(backup):
                raise RuntimeError(f'Missing backup: {backup}')
        elif exists(p) and p.read_text() != entry['content']:
            raise RuntimeError(f'Local settings changed; keep them and resolve manually: {p}')
    if dry:
        print(f'Would restore {len(data["entries"])} entries from {journal}')
        return
    for entry in reversed(data['entries']):
        p = Path(entry['target'])
        if exists(p):
            p.unlink()
        if entry.get('backup'):
            shutil.move(entry['backup'], p)
    data['rolled_back'] = True
    save(journal, data)
    print('Restored original configuration. Empty parent directories are retained.')

def install(home, dry=False, migrate=False, repair=False):
    # Validate sources and all parent directories before touching any configuration.
    planned = []
    for relative, target in LINKS.items():
        source, dest = ROOT / relative, home / target
        if not source.exists():
            raise RuntimeError(f'Missing source: {source}')
        for parent in dest.parents:
            if parent == home:
                break
            if parent.is_symlink() or (exists(parent) and not parent.is_dir()):
                raise RuntimeError(f'Parent must be a real directory: {parent}')
        if correct(dest, source):
            print(f'OK     {target}')
            continue
        if dest.is_symlink() and not repair:
            raise RuntimeError(f'Existing different link: {dest}; inspect it before using --repair-links')
        print(f'{"BACKUP" if exists(dest) else "LINK  "} {target}')
        planned.append((source, dest))
    local = home / '.config/zsh/local.zsh'
    private_lines = []
    if migrate and (home / '.zshrc').is_file():
        private_lines = PRIVATE.findall((home / '.zshrc').read_text())
        if private_lines and exists(local):
            old_local = local.read_text()
            if not all(line in old_local.splitlines() for line in private_lines):
                raise RuntimeError('local.zsh already exists and differs; merge local settings first.')
            private_lines = []
    if private_lines:
        print('LOCAL  migrate API/proxy assignments to ~/.config/zsh/local.zsh (values hidden)')
    if dry:
        print('Preview only; no files changed.')
        return
    if not planned and not private_lines:
        print('All links already correct; no new backup created.')
        return
    state = home / '.local/state/dotfiles'
    state.mkdir(parents=True, exist_ok=True)
    run = state / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    run.mkdir(mode=0o700)
    journal = run / 'journal.json'
    data = {'repository': str(ROOT), 'entries': []}
    save(journal, data)
    try:
        if private_lines:
            local.parent.mkdir(parents=True, exist_ok=True)
            content = '# Private machine settings; not tracked by Git.\n' + '\n'.join(private_lines) + '\n'
            # Journal before writing; exclusive create prevents overwriting existing files.
            data['entries'].append({'kind': 'local', 'target': str(local), 'content': content})
            save(journal, data)
            with open(local, 'x', opener=lambda path, flags: os.open(path, flags, 0o600)) as f:
                f.write(content)
        for i, (source, dest) in enumerate(planned):
            dest.parent.mkdir(parents=True, exist_ok=True)
            backup = run / f'{i:02d}-original' if exists(dest) else None
            if backup:
                shutil.move(str(dest), str(backup))
            entry = {'kind': 'link', 'source': str(source), 'target': str(dest), 'backup': str(backup) if backup else None}
            data['entries'].append(entry)
            save(journal, data)
            dest.symlink_to(source, target_is_directory=source.is_dir())
    except Exception:
        print(f'Installation interrupted. Recovery journal: {journal}', file=sys.stderr)
        rollback(journal)
        raise
    print(f'Installed. Recovery journal: {journal}')
    print(f'Rollback: python3 {ROOT / "scripts/install.py"} --rollback "{journal}"')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--home', type=Path, default=Path.home(), help='Target home (temporary homes for testing)')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--migrate-local', action='store_true', help='Preserve existing API and proxy exports outside Git')
    p.add_argument('--repair-links', action='store_true', help='Back up and replace existing links after inspection')
    p.add_argument('--rollback', type=Path)
    a = p.parse_args()
    if a.rollback:
        if json.loads(a.rollback.read_text()).get('rolled_back'):
            print('Already rolled back.')
            return
        rollback(a.rollback, a.dry_run)
    else:
        install(a.home.expanduser().absolute(), a.dry_run, a.migrate_local, a.repair_links)

if __name__ == '__main__':
    try:
        main()
    except (OSError, RuntimeError, ValueError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
