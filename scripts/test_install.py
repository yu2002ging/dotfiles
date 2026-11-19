"""Filesystem integration checks; no real user configurations are changed."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from install import install
from install import ROOT, LINKS

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
    def run_install(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(ROOT/'scripts/install.py'), '--home', str(self.home), *args], capture_output=True, text=True)
        self.assertEqual(p.returncode == 0, ok, p.stdout+p.stderr)
        return p
    def journals(self):
        return list(self.home.glob('.local/state/dotfiles/*/journal.json'))
    def test_interrupted_install_restores_original(self):
        original = "export ANTHROPIC_API_KEY='test-placeholder'\n"
        (self.home/'.zshrc').write_text(original)
        original_link = Path.symlink_to
        calls = []
        def fail_second(path, *args, **kwargs):
            calls.append(path)
            if len(calls) == 2:
                raise OSError('Simulated filesystem error')
            return original_link(path, *args, **kwargs)
        with patch.object(Path, 'symlink_to', fail_second):
            with self.assertRaises(OSError):
                install(self.home, migrate=True)
        self.assertEqual((self.home/'.zshrc').read_text(), original)
        self.assertFalse((self.home/'.config/zsh/local.zsh').exists())
        self.assertFalse((self.home/'.zprofile').exists())

    def test_dry_run(self):
        self.run_install('--dry-run')
        self.assertEqual(list(self.home.iterdir()), [])
    def test_backup_migrate_repeat_rollback(self):
        original = "export ANTHROPIC_API_KEY='test-placeholder'\nexport HTTP_PROXY=http://127.0.0.1:7892\n"
        (self.home/'.zshrc').write_text(original)
        n = self.home/'.config/nvim'; n.mkdir(parents=True); (n/'old.lua').write_text('original')
        self.run_install('--migrate-local')
        for src,dest in LINKS.items():
            self.assertEqual((self.home/dest).resolve(), (ROOT/src).resolve())
        local = self.home/'.config/zsh/local.zsh'
        self.assertIn('test-placeholder',local.read_text())
        self.assertEqual(local.stat().st_mode & 0o777, 0o600)
        j = self.journals()[0]
        self.run_install('--migrate-local')
        self.assertEqual(len(self.journals()),1)
        self.run_install('--rollback', str(j))
        self.assertEqual((self.home/'.zshrc').read_text(), original)
        self.assertEqual((n/'old.lua').read_text(),'original')
        self.assertFalse(local.exists())
        self.run_install('--rollback', str(j))
    def test_foreign_link_conflict_and_repair(self):
        other = self.home/'other'; other.write_text('keep')
        (self.home/'.zshrc').symlink_to(other)
        self.run_install(ok=False)
        self.assertFalse(self.journals())
        self.run_install('--repair-links')
        self.run_install('--rollback',str(self.journals()[0]))
        self.assertEqual((self.home/'.zshrc').resolve(),other.resolve())
    def test_rollback_protects_replaced_file(self):
        self.run_install()
        p=self.home/'.zshrc';p.unlink();p.write_text('new settings')
        self.run_install('--rollback',str(self.journals()[0]),ok=False)
        self.assertEqual(p.read_text(),'new settings')
    def test_parent_link_is_rejected(self):
        elsewhere=self.home/'elsewhere';elsewhere.mkdir()
        (self.home/'.config').symlink_to(elsewhere)
        self.run_install(ok=False)
        self.assertFalse(self.journals())
    def test_local_conflict_is_rejected_before_changes(self):
        (self.home/'.zshrc').write_text("export HTTP_PROXY=http://old\n")
        p=self.home/'.config/zsh/local.zsh';p.parent.mkdir(parents=True);p.write_text('keep')
        self.run_install('--migrate-local',ok=False)
        self.assertFalse((self.home/'.zshrc').is_symlink())
        self.assertFalse(self.journals())

if __name__ == '__main__':
    unittest.main()
