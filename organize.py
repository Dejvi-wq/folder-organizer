import argparse
import shutil
import sys
import time
from pathlib import Path

categories = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".odt": "Documents",
    ".xls": "Spreadsheets",
    ".xlsx": "Spreadsheets",
    ".xlsm": "Spreadsheets",
    ".csv": "Spreadsheets",
    ".ods": "Spreadsheets",
    ".ppt": "Presentations",
    ".pptx": "Presentations",
    ".odp": "Presentations",
    ".txt": "Text",
    ".rtf": "Text",
    ".md": "Text",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".webp": "Images",
    ".exe": "Installers",
    ".msi": "Installers",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".m4a": "Audio",
    ".flac": "Audio",
    ".mp4": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".mkv": "Videos",
}


def unique_destination(category_path, file_path):
    destination = category_path / file_path.name
    counter = 1
    while destination.exists():
        destination = category_path / f"{file_path.stem} ({counter}){file_path.suffix}"
        counter += 1
    return destination


def organize_directory(downloads_path, dry_run=False, min_age_minutes=2):
    if not downloads_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {downloads_path}")

    moved_count = 0
    for file_path in downloads_path.iterdir():
        if not file_path.is_file():
            continue

        category = categories.get(file_path.suffix.lower())
        if category is None:
            continue

        try:
            age_minutes = (time.time() - file_path.stat().st_mtime) / 60
            if min_age_minutes > 0 and age_minutes < min_age_minutes:
                print(f"Skipped recent file: {file_path.name}")
                continue

            category_path = downloads_path / category
            if not dry_run:
                category_path.mkdir(exist_ok=True)

            destination = unique_destination(category_path, file_path)
            if dry_run:
                print(f"Would move: {file_path.name} -> {category}/{destination.name}")
            else:
                shutil.move(str(file_path), str(destination))
                print(f"Moved: {file_path.name} -> {category}/{destination.name}")
            moved_count += 1
        except OSError as error:
            print(f"Could not move {file_path.name}: {error}", file=sys.stderr)

    return moved_count


def main():
    parser = argparse.ArgumentParser(description="Organize files in a Downloads folder.")
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.home() / "Downloads",
        help="folder to organize (defaults to your Downloads folder)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show planned moves without moving files",
    )
    parser.add_argument(
        "--min-age-minutes",
        type=float,
        default=2,
        help="skip files modified more recently than this many minutes (default: 2)",
    )
    args = parser.parse_args()

    if args.min_age_minutes < 0:
        parser.error("--min-age-minutes must be zero or greater")

    try:
        count = organize_directory(
            args.directory,
            dry_run=args.dry_run,
            min_age_minutes=args.min_age_minutes,
        )
    except (NotADirectoryError, OSError) as error:
        print(error, file=sys.stderr)
        return 1

    action = "would be organized" if args.dry_run else "organized"
    print(f"{count} file(s) {action}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())