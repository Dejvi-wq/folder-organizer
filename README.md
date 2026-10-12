# folder-organizer

A Python command-line tool that sorts files in your Downloads folder into category folders. It can also organize another folder you specify.

## Requirements

- Python 3.8 or newer
- Windows, macOS, or Linux

The project uses only Python's standard library; no packages need to be installed.

## Preview and run

Open a terminal in the folder containing `organize.py`. Preview the planned moves first:

```powershell
python organize.py --dry-run
```

Organize your Downloads folder:

```powershell
python organize.py
```

Organize a different folder by passing its path:

```powershell
python organize.py "C:\Users\you\Downloads" --dry-run
python organize.py "C:\Users\you\Downloads"
```

By default, files modified in the last two minutes are skipped to reduce the chance of moving an active download. Change the delay or disable it with `--min-age-minutes`:

```powershell
python organize.py --min-age-minutes 5
python organize.py --min-age-minutes 0
```

`--dry-run` can be combined with a directory path or age setting. A normal run moves files, so preview first if you are unsure.

## File categories

| Extensions | Destination folder |
| `.pdf`, `.doc`, `.docx`, `.odt` | `Documents` |
| `.xls`, `.xlsx`, `.xlsm`, `.csv`, `.ods` | `Spreadsheets` |
| `.ppt`, `.pptx`, `.odp` | `Presentations` |
| `.txt`, `.rtf`, `.md` | `Text` |
| `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp` | `Images` |
| `.exe`, `.msi` | `Installers` |
| `.zip`, `.rar`, `.7z`, `.tar`, `.gz` | `Archives` |
| `.mp3`, `.wav`, `.m4a`, `.flac` | `Audio` |
| `.mp4`, `.mov`, `.avi`, `.mkv` | `Videos` |

Extensions are matched without regard to letter case. Directories and unlisted file types are left alone. If the destination already contains a file with the same name, the organizer adds a number to the new filename instead of replacing the existing file. A move error is reported and the organizer continues with other files.

## Run tests

From the project folder, run:

```powershell
python -m unittest discover -s tests
```

The tests use temporary folders and do not move files from your Downloads folder.

## Run automatically on Windows

You can use Task Scheduler to run the organizer at sign-in and periodically afterward:

1. Open **Task Scheduler** and choose **Create Task**.
2. On **General**, name the task `Downloads Folder Organizer` and select **Run only when user is logged on**.
3. On **Triggers**, add an **At log on** trigger. Set it to repeat every 15 minutes, with the duration set to **Indefinitely** if available.
4. On **Actions**, choose **Start a program**. Set **Program/script** to the Python executable path shown by `where.exe python` in PowerShell.
5. Set **Add arguments** to `"C:\Users\you\folder-organizer\organize.py" --min-age-minutes 2`, replacing the example path with the actual location of this project.
6. Set **Start in** to the project folder, such as `C:\Users\you\folder-organizer`.
7. Save the task. Check its **History** tab if it does not run as expected.

Scheduled runs move files automatically. Preview with `--dry-run` before enabling the task, and make sure the arguments and folder path are correct.