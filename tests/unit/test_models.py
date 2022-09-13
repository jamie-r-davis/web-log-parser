from pathlib import Path

import pytest
from apachelogs import LogEntry

from config import Config
from src.models import LogFile, LogRecord


@pytest.fixture
def log_file():
    return LogFile("sample_443.gz", Config.LOG_FORMAT)


def test_logfile_domain():
    lf1 = LogFile("sample-443.120101.gz", "")
    assert lf1.domain == "sample"
    lf2 = LogFile("sample.dev.120323.gz", "")
    assert lf2.domain == "sample.dev"
    lf3 = LogFile("sample.dev.alumni-443.120123.gz", "")
    assert lf3.domain == "sample.dev.alumni"


def test_logfile_protocol():
    lf1 = LogFile("sample-443.120101.gz", "")
    assert lf1.protocol == "https"
    lf2 = LogFile("sample.dev.120323.gz", "")
    assert lf2.protocol == "http"
    lf3 = LogFile("sample.dev.alumni-443.120123.gz", "")
    assert lf3.protocol == "https"


def test_logfile_entries(log_file):
    entry = next(log_file.entries)
    assert isinstance(entry, LogRecord)
    assert entry.id == "sample_443.gz-1"
