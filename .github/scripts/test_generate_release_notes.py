import os
import shutil
import unittest
from generate_release_notes import generate_release_notes

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

if __name__ == "__main__":
    unittest.main()
