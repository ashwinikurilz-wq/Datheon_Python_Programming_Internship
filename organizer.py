
import os
import shutil
from pathlib import Path

# File extensions and their destination folders
FILE_CATEGORIES = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",

    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".odt": "Documents",
    ".epub": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",
    ".bmp": "Images",
    ".svg": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",
    ".wmv": "Videos",

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".aac": "Audio",
    ".flac": "Audio",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Code
    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".sql": "Code",

    # Spreadsheets
    ".csv": "Spreadsheets",
    ".xls": "Spreadsheets",
    ".xlsx": "Spreadsheets",

    # Presentations
    ".ppt": "Presentations",
    ".pptx": "Presentations",
}



def unique_destination(destination):
    """Avoid overwriting files with the same name."""
    if not destination.exists():
        return destination

    folder = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        new_path = folder / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def organize_folder(folder_path):
    folder = Path(folder_path).expanduser().resolve()

    if not folder.is_dir():
        print("Error: The specified folder does not exist.")
        return

    moved = 0
    skipped = 0
    errors = 0

    print(f"\nOrganizing folder: {folder}\n")

    try:
        entries = list(os.scandir(folder))
    except PermissionError:
        print("Error: Permission denied when accessing this folder.")
        return

    for entry in entries:
        if not entry.is_file(follow_symlinks=False):
            continue

        source = Path(entry.path)
        category = FILE_CATEGORIES.get(
            source.suffix.lower(), "Others"
        )
        destination_folder = folder / category

        try:
            destination_folder.mkdir(exist_ok=True)
            destination = unique_destination(
                destination_folder / source.name
            )
            shutil.move(str(source), str(destination))
            print(f"Moved: {source.name} -> {category}/{destination.name}")
            moved += 1

        except PermissionError:
            print(f"Permission denied: {source.name}")
            errors += 1
        except OSError as error:
            print(f"Could not move {source.name}: {error}")
            errors += 1

    print("\n========== ORGANIZATION SUMMARY ==========")
    print(f"Files moved successfully: {moved}")
    print(f"Files skipped: {skipped}")
    print(f"Errors: {errors}")
    print("Organization complete!")


if __name__ == "__main__":
    target = input(
        "Enter the folder path to organize: "
    ).strip().strip('"')

    if target:
        organize_folder(target)
    else:
        print("No folder path provided.")
