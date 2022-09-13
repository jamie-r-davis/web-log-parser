from typing import Iterator

from sqlalchemy import Column, DateTime, Index, Integer, MetaData, String, Table, func
from sqlalchemy.orm import Session, registry

from src.models import LogFile, LogRecord

mapper_registry = registry()
metadata_obj = MetaData()

log_entry = Table(
    "log_entry",
    metadata_obj,
    Column("id", String(60), primary_key=True, sqlite_on_conflict_primary_key="IGNORE"),
    Column("domain", String(200), nullable=False, index=True),
    Column("timestamp", DateTime, nullable=False),
    Column("remote_host", String(200), nullable=False),
    Column("method", String(6)),
    Column("status_code", Integer, nullable=False),
    Column("protocol", String(5), nullable=False),
    Column("uri", String()),
    Column("request_duration", Integer),
    Column("referer", String()),
    Column("user_agent", String(200)),
)

Index(
    "ix_log_entry__domain_date_status_code",
    log_entry.c.domain,
    func.date(log_entry.c.timestamp),
    log_entry.c.status_code,
),
Index(
    "ix_log_entry__protocol_status_code",
    log_entry.c.protocol,
    log_entry.c.status_code,
)


def start_mappers():
    mapper_registry.map_imperatively(LogRecord, log_entry)


def bulk_insert_entries(session: Session, entries: Iterator[LogRecord]):
    entry_mappings = (e.__dict__ for e in entries)
    session.bulk_insert_mappings(
        LogRecord, entry_mappings, return_defaults=False, render_nulls=True
    )
    session.commit()
