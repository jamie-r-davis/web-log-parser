import logging
from pathlib import Path
from typing import Iterator, Union

from src.models import LogFile, LogRecord
from src.utils import ensure_path


def parse_domain(domain_path: Union[Path, str], log_fmt: str) -> Iterator[LogRecord]:
    """Iterates over all log files within the domain directory, returning an iterator of LogRecords"""
    for file in sorted(
        ensure_path(domain_path).rglob("*.gz"), key=lambda x: str(x.absolute())
    ):
        logging.info(f"Parsing {file.name}")
        log_file = LogFile(file, log_fmt)
        for log_record in log_file.entries:
            yield log_record


def parse_glob_entries(
    data_dir: Union[Path, str], glob: str, log_fmt: str
) -> Iterator[LogRecord]:
    for file in sorted(Path(data_dir).rglob(glob), key=lambda x: str(x.absolute())):
        logging.info(f"Parsing {file.name}")
        log_file = LogFile(file, log_fmt)
        for log_record in log_file.entries:
            yield log_record
