import os


class Config:

    # the number of records to insert/commit to the database at a time
    CHUNKSIZE = 10_000

    # the connection string for your database,
    # see https://docs.sqlalchemy.org/en/14/core/engines.html
    DB_URI = os.getenv("DB_URI", "sqlite:///logs-sam-demo.db")

    # when true, will print all sql statements to stdout
    DB_ECHO = bool(os.getenv("DB_ECHO", False))

    # the log format passed to the apachelogs LogParser
    # see https://apachelogs.readthedocs.io/en/stable/directives.html
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT", '%h %l %u %t "%r" %s %b "%{Referer}i" "%{User-agent}i" %D'
    )

    # the path to the directory containing your log files
    # pass either an absolute path or a path relative to the root
    # of this project
    DATA_DIR = os.getenv("DATA_DIR", "/Users/jamjam/webhosting-logs/domains")
