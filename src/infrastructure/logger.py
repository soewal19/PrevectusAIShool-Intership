
import logging
import sys
import zipfile
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "log"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE_PREFIX = "claude_analytics"
ACTIVE_LOG_NAME = f"{LOG_FILE_PREFIX}.log"
MAX_VISIBLE_LOG_FILES = 5
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(lineno)d | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logging_configured = False


def _active_log_path() -> Path:
    return LOG_DIR / ACTIVE_LOG_NAME


def _timestamped_log_path() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return LOG_DIR / f"{LOG_FILE_PREFIX}_{timestamp}.log"


def _list_plain_logs() -> list[Path]:
    return sorted(
        [path for path in LOG_DIR.glob(f"{LOG_FILE_PREFIX}*.log") if path.is_file()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def _rotate_active_log() -> None:
    active_log = _active_log_path()
    if not active_log.exists():
        return

    if active_log.stat().st_size == 0:
        active_log.unlink()
        return

    active_log.rename(_timestamped_log_path())


def _archive_old_logs() -> None:
    visible_logs = _list_plain_logs()
    logs_to_archive = visible_logs[MAX_VISIBLE_LOG_FILES:]
    if not logs_to_archive:
        return

    archive_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = LOG_DIR / f"{LOG_FILE_PREFIX}_archive_{archive_timestamp}.zip"

    with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for log_path in logs_to_archive:
            archive.write(log_path, arcname=log_path.name)

    for log_path in logs_to_archive:
        log_path.unlink()


def configure_logging() -> None:
    global _logging_configured
    if _logging_configured:
        return

    _rotate_active_log()
    _archive_old_logs()

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    file_handler = logging.FileHandler(_active_log_path(), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    if sys.platform == "win32":
        import io
        console_handler.stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _logging_configured = True


def get_logger(name: str) -> logging.Logger:
    if not _logging_configured:
        configure_logging()
    return logging.getLogger(name)
