import io
import os
import shutil
import unittest
from unittest.mock import patch
from generate_release_notes import generate_release_notes
from format_telegram_summary import format_telegram_summary, main

class TestGenerateReleaseNotes(unittest.TestCase):
    def setUp(self):
        self.test_dir = "build_test_mock"
        os.makedirs(self.test_dir, exist_ok=True)
        self.mock_build_md = "mock_build.md"
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.mock_build_md):
            os.remove(self.mock_build_md)

    def write_build_md(self, content):
        with open(self.mock_build_md, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def create_artifacts(self, filenames):
        for f in filenames:
            open(os.path.join(self.test_dir, f), 'w').close()

    def test_single_ecosystem(self):
        self.write_build_md("Patches: MorpheApp/patches-v1.39.1.mpp")
        self.create_artifacts(["youtube-morphe-v21.04.223-all.apk"])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("Morphe 1.39.1", title)
        self.assertIn("Successfully generated **1** build variants", body)
        self.assertIn("Youtube Morphe | 21.04.223 | all | APK", body)
        
    def test_multiple_ecosystems(self):
        self.write_build_md("Patches: MorpheApp/patches-1.39.1\nPatches: crimera/piko-v1.0.0")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("Morphe & Piko Release", title)

    def test_missing_patch_metadata(self):
        self.write_build_md("Skipped:\nNothing")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("Modules Release", title)

    def test_multiple_patch_versions(self):
        self.write_build_md("Patches: MorpheApp/patches-1.39.1\nPatches: MorpheApp/patches-1.40.0")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("Morphe Release", title)

    def test_no_artifacts(self):
        self.write_build_md("Patches: MorpheApp/patches-1.39.1")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("No apps were successfully generated", body)
        
    def test_missing_build_md(self):
        self.create_artifacts(["youtube-morphe-v21.04.223-all.apk"])
        # Do not create build.md
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path="nonexistent_build.md")
        self.assertIn("Modules Release", title)
        self.assertIn("Successfully generated **1** build variants", body)
        self.assertIn("Youtube Morphe | 21.04.223 | all | APK", body)

    def test_architectures_and_qualifiers(self):
        self.write_build_md("")
        self.create_artifacts([
            "music-morphe-v9.15.51-arm64-v8a.apk",
            "music-morphe-module-v9.15.51-arm64-v8a.zip",
            "music-morphe-v9.15.51-arm-v7a.apk",
            "some-app-v1.0.0-rc1-x86.apk",
            "some-app-v1.0.0-rc1-x86_64.apk",
            "random-non-matching-file.txt"
        ])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("Successfully generated **4** build variants", body)
        self.assertIn("Music Morphe | 9.15.51 | arm64-v8a | APK, Module", body)
        self.assertIn("Music Morphe | 9.15.51 | arm-v7a | APK", body)
        self.assertIn("Some App | 1.0.0-rc1 | x86 | APK", body)
        self.assertIn("Some App | 1.0.0-rc1 | x86_64 | APK", body)
        self.assertNotIn("random", body)
        
    def test_skipped_entries(self):
        self.write_build_md("Skipped:\nTwitch (disabled)")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("## Skipped / Failed", body)
        self.assertIn("- Twitch (disabled)", body)

    def test_devanced_and_patch_set_formatting(self):
        self.write_build_md("Patches: RookieEnough/De-Vanced/patches-v1.0.0.mpp")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("DeVanced 1.0.0", title)
        self.assertIn("- **RookieEnough/De-Vanced**: `patches-v1.0.0.mpp`", body)

    def test_wagg13_and_patch_set_formatting(self):
        self.write_build_md("Patches: WaggBR/Wagg13Patch_Morphe/patches-1.0.0.mpp")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("Wagg13 1.0.0", title)
        self.assertIn("- **WaggBR/Wagg13Patch_Morphe**: `patches-1.0.0.mpp`", body)

    def test_failed_app_reporting(self):
        self.write_build_md("Skipped:\n- Tinder-Wagg13 17.34.1: stock APK download failed")
        self.create_artifacts([])
        title, body = generate_release_notes(build_dir=self.test_dir, build_md_path=self.mock_build_md)
        self.assertIn("## Skipped / Failed", body)
        self.assertIn("- Tinder-Wagg13 17.34.1: stock APK download failed", body)

class TestFormatTelegramSummary(unittest.TestCase):
    def test_normal_link(self):
        src = "[Normal](https://example.com)"
        expected = '<a href="https://example.com">Normal</a>'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_text_surrounding_link(self):
        src = "Text before [Link](https://example.com/path) text after"
        expected = 'Text before <a href="https://example.com/path">Link</a> text after'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_ampersand_in_label_and_url(self):
        src = "[Test & Stuff](https://example.com/?a=1&b=2)"
        expected = '<a href="https://example.com/?a=1&amp;b=2">Test &amp; Stuff</a>'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_unsafe_text_surrounding_link(self):
        src = "<unsafe> & [safe](https://example.com)"
        expected = '&lt;unsafe&gt; &amp; <a href="https://example.com">safe</a>'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_malformed_url_scheme(self):
        src = "[broken](not-a-valid-url)"
        expected = "[broken](not-a-valid-url)"
        self.assertEqual(format_telegram_summary(src), expected)

    def test_unfinished_link(self):
        src = "[unfinished](https://example.com"
        expected = "[unfinished](https://example.com"
        self.assertEqual(format_telegram_summary(src), expected)

    def test_label_with_html_tags(self):
        src = "[<tag> & 'quote'](https://example.com)"
        expected = '<a href="https://example.com">&lt;tag&gt; &amp; \'quote\'</a>'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_url_with_quotes(self):
        src = '[Link](https://example.com/foo"bar)'
        expected = '<a href="https://example.com/foo&quot;bar">Link</a>'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_balanced_parentheses_in_url(self):
        src = "[Wiki](https://en.wikipedia.org/wiki/Foo_(bar))"
        expected = '<a href="https://en.wikipedia.org/wiki/Foo_(bar)">Wiki</a>'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_multiple_links_on_same_line(self):
        src = "Visit [Site A](https://a.com) and [Site B](https://b.com)!"
        expected = 'Visit <a href="https://a.com">Site A</a> and <a href="https://b.com">Site B</a>!'
        self.assertEqual(format_telegram_summary(src), expected)

    def test_real_build_md_snippet(self):
        src = (
            "Install [Microg](https://github.com/MorpheApp/MicroG-RE/) for non-root YouTube and YT Music APKs\n"
            "Use [zygisk-detach](https://github.com/j-hc/zygisk-detach) to detach YouTube and YT Music modules from Play Store\n\n"
            "[revanced-magisk-module](https://github.com/j-hc/revanced-magisk-module)\n\n"
            "Patches: crimera/piko-newx/patches-3.47.0.mpp\n"
            "[Changelog](https://github.com/crimera/piko-newx/releases/tag/v3.47.0)"
        )
        expected = (
            'Install <a href="https://github.com/MorpheApp/MicroG-RE/">Microg</a> for non-root YouTube and YT Music APKs\n'
            'Use <a href="https://github.com/j-hc/zygisk-detach">zygisk-detach</a> to detach YouTube and YT Music modules from Play Store\n\n'
            '<a href="https://github.com/j-hc/revanced-magisk-module">revanced-magisk-module</a>\n\n'
            'Patches: crimera/piko-newx/patches-3.47.0.mpp\n'
            '<a href="https://github.com/crimera/piko-newx/releases/tag/v3.47.0">Changelog</a>'
        )
        self.assertEqual(format_telegram_summary(src), expected)

    def test_main_cli_file(self):
        tmp_file = "test_cli_summary.md"
        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write("[Example](https://example.com)")
            with patch("sys.argv", ["format_telegram_summary.py", tmp_file]):
                with patch("sys.stdout", new=io.StringIO()) as fake_out:
                    main()
                    self.assertEqual(fake_out.getvalue(), '<a href="https://example.com">Example</a>')
        finally:
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

    def test_main_cli_stdin(self):
        with patch("sys.argv", ["format_telegram_summary.py"]):
            with patch("sys.stdin", new=io.StringIO("[Stdin](https://stdin.com)")):
                with patch("sys.stdout", new=io.StringIO()) as fake_out:
                    main()
                    self.assertEqual(fake_out.getvalue(), '<a href="https://stdin.com">Stdin</a>')


if __name__ == "__main__":
    unittest.main()
