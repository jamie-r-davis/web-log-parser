import gzip
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

from apachelogs import InvalidEntryError, LogEntry, LogParser

from src.utils import ensure_path


@dataclass
class LogRecord:
    id: str
    domain: str
    timestamp: datetime
    remote_host: str
    status_code: int
    protocol: str
    request_duration: int
    uri: Optional[str]
    method: Optional[str]
    referer: Optional[str]
    user_agent: Optional[str]

    @classmethod
    def from_entry(cls, id: str, domain: str, protocol: str, entry: LogEntry):
        method = None
        uri = None
        if isinstance(entry.request_line, str):
            method, uri, *_ = entry.request_line.split(" ")

        return cls(
            id=id,
            domain=domain,
            timestamp=entry.request_time,
            remote_host=entry.remote_host,
            method=method,
            status_code=entry.status,
            protocol=protocol,
            uri=uri,
            request_duration=entry.request_duration_microseconds,
            referer=entry.headers_in.get("Referer"),
            user_agent=entry.headers_in.get("User-Agent"),
        )


class LogFile:
    def __init__(self, filepath: Path, log_format: str):
        self.filepath = ensure_path(filepath)
        self.log_format = log_format
        self._domain: Optional[str] = None
        self._protocol: Optional[str] = None

    @property
    def domain(self) -> str:
        if self._domain is None:
            pattern = r"^(?P<domain>.+?)(?:-443)?\.\d{6}\.gz$"
            matches = re.match(pattern, self.filepath.name)
            if matches:
                self._domain = matches.groupdict().get("domain")
            else:
                self._domain = self.filepath.name
        return self._domain

    @property
    def protocol(self) -> str:
        if self._protocol is None:
            self._protocol = "https" if "443" in self.filepath.name else "http"
        return self._protocol

    @property
    def entries(self) -> Iterator[LogRecord]:
        """Parses the log file, returning an iterator of LogRecords"""
        parser = LogParser(self.log_format)
        with gzip.open(self.filepath, "rt") as file:
            for i, line in enumerate(file):
                id_ = f"{self.filepath.name}-{i+1}"
                try:
                    entry = parser.parse(line)
                    log_record = LogRecord.from_entry(
                        id=id_, domain=self.domain, protocol=self.protocol, entry=entry
                    )
                except (InvalidEntryError, ValueError) as e:
                    logging.error(e)
                else:
                    yield log_record
