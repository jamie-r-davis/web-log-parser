import gzip
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterator, Union

import apachelogs
import pandas as pd

DOMAIN_DIR = (
    "/Users/jamjam/Dropbox (University of Michigan)/wolverine-webhosting/http_https"
)
LOG_FORMAT = '%h %l %u %t "%r" %s %b "%{Referer}i" "%{User-agent}i" %D'
DOMAIN_REGEX = re.compile(r"^(?P<domain>.+?)(?P<protocol>[\-:\/]443)?\.\d{6}\.gz$")


def parse_filepath(filepath: Union[str, Path]) -> tuple[str, str]:
    filepath = Path(filepath)
    match_group = DOMAIN_REGEX.fullmatch(filepath.name)
    if match_group is None:
        raise ValueError(f"Could not parse filename: {filepath.name}")
    domain = match_group.groupdict().get("domain")
    protocol = "https" if match_group.groupdict().get("protocol") else "http"
    return domain, protocol


def request_uri_is_valid(entry: apachelogs.LogEntry) -> bool:
    method, uri, protocol = entry.request_line.split(" ")
    if "favicon" in uri:
        return False
    if "robots.txt" in uri:
        return False
    if ".well-known" in uri:
        return False
    return True


def flatten_domain_dict(obj: dict) -> Iterator[dict]:
    for k, v in obj.items():
        yield {"domain": k, "http": v["http"], "https": v["https"]}


def main():
    domains = defaultdict(lambda: {"http": None, "https": None})
    prev_domain = None
    parser = apachelogs.LogParser(LOG_FORMAT)
    for filepath in sorted(
        Path(DOMAIN_DIR).rglob("*.gz"), key=lambda x: str(x.absolute())
    ):
        domain, protocol = parse_filepath(filepath)
        if domain != prev_domain:
            print(f"Scanning {domain}...")
        if domains[domain][protocol]:
            continue

        with gzip.open(filepath, "rt") as file:
            for entry in parser.parse_lines(file, ignore_invalid=True):
                if 200 <= entry.status < 300 and entry.request_line:
                    try:
                        if request_uri_is_valid(entry):
                            domains[domain][protocol] = True
                            print(f"  👍{protocol}")
                            break
                    except ValueError:
                        pass
                else:
                    domains[domain][protocol] = False

        prev_domain = domain

    df = pd.DataFrame(flatten_domain_dict(domains))
    df.to_csv("http_https_result.csv", header=True, index=False)


if __name__ == "__main__":
    main()
