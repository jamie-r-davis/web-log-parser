import logging

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Config
from src import orm
from src.models import LogRecord
from src.orm import bulk_insert_entries
from src.parsers import parse_domain, parse_glob_entries
from src.utils import clear_lines, collect_domains, grouper

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
logger = logging.getLogger()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("domains", nargs=-1)
@click.option(
    "--drop",
    is_flag=True,
    show_default=True,
    default=False,
    help="Drop log_entry table before parsing files",
)
def parse(domains: tuple, drop: bool):
    db = create_engine(Config.DB_URI, echo=Config.DB_ECHO)
    orm.metadata_obj.bind = db
    if drop:
        try:
            orm.log_entry.drop()
        except Exception:
            pass
    orm.metadata_obj.create_all(db)
    orm.start_mappers()
    session = Session(db)

    domain_paths = collect_domains(domains, Config.DATA_DIR)
    print("Parsing domains: {}...".format(", ".join(x.name for x in domain_paths)))
    for domain in domain_paths:
        print(f"Parsing {domain.name}...")
        entries = parse_domain(domain, Config.LOG_FORMAT)
        for i, chunk in enumerate(grouper(Config.CHUNKSIZE, entries)):
            if i > 0:
                clear_lines()
            session.bulk_insert_mappings(
                LogRecord, [record.__dict__ for record in chunk]
            )
            session.commit()
            print(f"  - {(i+1)*Config.CHUNKSIZE:,} records inserted")


@cli.command()
@click.argument("glob_pattern", type=click.STRING)
@click.option(
    "--drop",
    is_flag=True,
    show_default=True,
    default=False,
    help="Drop log_entry table before parsing files",
)
def parse_glob(glob_pattern: str, drop: bool):
    db = create_engine(Config.DB_URI, echo=Config.DB_ECHO)
    orm.metadata_obj.bind = db
    if drop:
        try:
            orm.log_entry.drop()
        except Exception:
            pass
    orm.metadata_obj.create_all(db)
    orm.start_mappers()
    session = Session(db)
    entries = parse_glob_entries(Config.DATA_DIR, glob_pattern, Config.LOG_FORMAT)
    for i, chunk in enumerate(grouper(Config.CHUNKSIZE, entries)):
        if i > 0:
            clear_lines()
        bulk_insert_entries(session, chunk)
        print(f"  - {(i + 1) * Config.CHUNKSIZE:,} records inserted")


if __name__ == "__main__":
    cli()
