"""Unit tests for static CSS fixes and reversible profile installation (not GUI tests)."""
from pathlib import Path
import json
import tempfile
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from kur import install
from geri_al import restore
from fix_shyfox_159 import patch_css

class Patches(unittest.TestCase):
    def test_upstream_patch_250(self):
        for name in ('shy-global.css','shy-navbar.css','shy-sidebar.css','shy-toolbar.css'):
            css = (ROOT/'chrome'/'ShyFox'/name).read_text(encoding='utf-8')
            self.assertNotIn('[chromehidden=""]', css, name)
            self.assertIn('[popup-window]', css, name)
            self.assertEqual(patch_css(name,css)[0],css)

    def test_findbar_patch_243(self):
        css=(ROOT/'chrome'/'ShyFox'/'shy-findbar.css').read_text(encoding='utf-8')
        self.assertIn('left: 50% !important;',css)
        self.assertIn('transform: translateX(-50%) !important;',css)
        self.assertEqual(patch_css('shy-findbar.css',css)[0],css)

    def test_bundle(self):
        self.assertTrue((ROOT/'chrome'/'userChrome.css').is_file())
        self.assertTrue((ROOT/'chrome'/'userContent.css').is_file())
        self.assertIn('Mozilla Public License Version 2.0',(ROOT/'LICENSE').read_text())
        json.loads((ROOT/'sidebery-settings.json').read_text())

class Installer(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.profile=Path(self.temp.name)/'test.default-release'
        self.profile.mkdir()
        (self.profile/'prefs.js').write_text('// test prefs\n')

    def test_dry_run(self):
        count,backup=install(self.profile,dry_run=True,check_process=False)
        self.assertGreater(count,0)
        self.assertIsNone(backup)
        self.assertFalse((self.profile/'chrome').exists())

    def test_install_restore_existing(self):
        css=self.profile/'chrome'/'userChrome.css'
        css.parent.mkdir()
        css.write_text('/* private theme */\n')
        (self.profile/'user.js').write_text('// private prefs\n')
        count,backup=install(self.profile,include_user_js=True,check_process=False)
        self.assertGreater(count,0)
        self.assertIsNotNone(backup)
        self.assertEqual((self.profile/'user.js').read_text(),'// private prefs\n')
        self.assertEqual(install(self.profile,check_process=False)[0],0)
        todo,conflicts=restore(self.profile,backup,dry_run=True,check_process=False)
        self.assertGreater(todo,0)
        self.assertEqual(conflicts,0)
        restored,conflicts=restore(self.profile,backup,check_process=False)
        self.assertEqual(restored,todo)
        self.assertEqual(conflicts,0)
        self.assertEqual(css.read_text(),'/* private theme */\n')
        self.assertFalse((self.profile/'chrome'/'ShyFox'/'shy-global.css').exists())

    def test_restore_preserves_later_changes(self):
        _,backup=install(self.profile,check_process=False)
        target=self.profile/'chrome'/'userChrome.css'
        target.write_text('/* custom changes */\n')
        _,conflicts=restore(self.profile,backup,check_process=False)
        self.assertEqual(conflicts,1)
        self.assertEqual(target.read_text(),'/* custom changes */\n')

    def test_user_js_opt_in(self):
        install(self.profile,check_process=False)
        self.assertFalse((self.profile/'user.js').exists())
        _,backup=install(self.profile,include_user_js=True,check_process=False)
        self.assertTrue((self.profile/'user.js').is_file())
        restore(self.profile,backup,check_process=False)
        self.assertFalse((self.profile/'user.js').exists())

if __name__=='__main__': unittest.main()
