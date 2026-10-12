import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from organize import organize_directory


class OrganizeDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.downloads_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def organize_quietly(self, dry_run=False, min_age_minutes=0):
        with contextlib.redirect_stdout(io.StringIO()):
            return organize_directory(
                self.downloads_path,
                dry_run=dry_run,
                min_age_minutes=min_age_minutes,
            )

    def test_moves_files_into_matching_category(self):
        source = self.downloads_path / "report.PDF"
        source.write_text("sample")

        self.assertEqual(self.organize_quietly(), 1)
        self.assertTrue((self.downloads_path / "Documents" / "report.PDF").is_file())
        self.assertFalse(source.exists())

    def test_dry_run_does_not_move_or_create_category(self):
        source = self.downloads_path / "photo.jpg"
        source.write_text("sample")

        self.assertEqual(self.organize_quietly(dry_run=True), 1)
        self.assertTrue(source.is_file())
        self.assertFalse((self.downloads_path / "Images").exists())

    def test_sorts_office_documents_and_spreadsheets(self):
        word_file = self.downloads_path / "notes.docx"
        excel_file = self.downloads_path / "budget.xlsx"
        word_file.write_text("sample")
        excel_file.write_text("sample")

        self.assertEqual(self.organize_quietly(), 2)
        self.assertTrue((self.downloads_path / "Documents" / "notes.docx").is_file())
        self.assertTrue((self.downloads_path / "Spreadsheets" / "budget.xlsx").is_file())

    def test_skips_recent_files_with_default_age_threshold(self):
        source = self.downloads_path / "recent.docx"
        source.write_text("sample")

        self.assertEqual(self.organize_quietly(min_age_minutes=2), 0)
        self.assertTrue(source.is_file())

        self.assertEqual(self.organize_quietly(min_age_minutes=0), 1)
        self.assertTrue((self.downloads_path / "Documents" / "recent.docx").is_file())

    def test_duplicate_name_gets_a_numbered_destination(self):
        category_path = self.downloads_path / "Archives"
        category_path.mkdir()
        (category_path / "backup.zip").write_text("existing")
        (self.downloads_path / "backup.zip").write_text("new")

        self.assertEqual(self.organize_quietly(), 1)
        self.assertEqual((category_path / "backup.zip").read_text(), "existing")
        self.assertEqual((category_path / "backup (1).zip").read_text(), "new")

    def test_ignores_unknown_extensions_and_directories(self):
        unknown_file = self.downloads_path / "notes.bin"
        unknown_file.write_text("sample")
        nested_folder = self.downloads_path / "already-organized"
        nested_folder.mkdir()

        self.assertEqual(self.organize_quietly(), 0)
        self.assertTrue(unknown_file.is_file())
        self.assertTrue(nested_folder.is_dir())

    def test_rejects_a_missing_directory(self):
        missing_path = self.downloads_path / "missing"

        with self.assertRaises(NotADirectoryError):
            organize_directory(missing_path)


if __name__ == "__main__":
    unittest.main()