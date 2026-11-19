#!/usr/bin/env python3
"""Inspect links without changing configuration."""
import argparse
from pathlib import Path
import shutil
from install import ROOT, LINKS, correct

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--home', type=Path, default=Path.home())
a = p.parse_args()
failed = False
for src, dest in LINKS.items():
    ok = correct(a.home / dest, ROOT / src)
    print(f'{"OK" if ok else "FIX"} {dest}')
    failed |= not ok
for tool in ['git', 'python3', 'zsh', 'brew', 'nvim', 'fzf', 'zoxide', 'starship']:
    print(f'{"FOUND" if shutil.which(tool) else "MISSING"} {tool}')
print('Local settings:', 'present' if (a.home / '.config/zsh/local.zsh').is_file() else 'absent (optional)')
raise SystemExit(1 if failed else 0)
