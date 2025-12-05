import shutil
import logging
from pathlib import Path

# --- CONFIGURATION ---
# MAPPING: Windows Extensions to Categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".git", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Executables": [".exe", ".msi", ".bat"],
}

# --- LOGGING SETUP ---
# Ensure the logs directory exists before writing
log_dir = Path("../logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "cleanup.log"),
        logging.StreamHandler(),
    ],
)


def get_windows_downloads_path():
    # username = "User"
    path = Path("/mnt/d/Downloads")
    return path


def organize_directory(path: Path):
    if not path.exists():
        logging.error(f"CRITICAL: Directory not found: {path}")
        logging.error("Did you update the username in script?")
        return

    logging.info(f"Target Acquired: {path}")
    logging.info("Scanning for the files...")

    files_moved = 0

    for file in path.iterdir():
        if file.is_dir():
            continue

        if (
            file.name.startswith(".")
            or file.suffix == ".tmp"
            or file.suffix == ".crdownload"
        ):
            continue

        file_extension = file.suffix.lower()
        destination_folder = "Others"

        for category, extensions in FILE_TYPES.items():
            if file_extension in extensions:
                destination_folder = category
                break

        target_dir = path / destination_folder
        target_dir.mkdir(exist_ok=True)
        destination_path = target_dir / file.name

        try:
            if destination_path.exists():
                logging.warning(
                    f"Collision: {file.name} exists in {destination_folder}. Skipping..."
                )
            else:
                shutil.move(str(file), str(destination_path))
                logging.info(f"Moved: {file.name} -> {destination_folder}")
                files_moved += 1
        except Exception as e:
            logging.error(f"Error on {file.name}: {e}")

    logging.info(f"Operation Complete. Total files moved {files_moved}.")


if __name__ == "__main__":
    target_path = get_windows_downloads_path()

    print(f"WARNING: About to reorganize: {target_path}")
    confirm = input("Are you sure for files organization? ( y / n ): ")

    if confirm.lower() == "y":
        organize_directory(target_path)
    else:
        print("Aborted")
