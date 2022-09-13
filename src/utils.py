import itertools
from pathlib import Path
from typing import Union


def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def ensure_path(filepath: Union[str, Path]) -> Path:
    if not isinstance(filepath, Path):
        return Path(filepath)
    return filepath


def clear_lines(n_lines: int = 1):
    LINE_UP = "\033[1A"
    LINE_CLEAR = "\x1b[2K"
    for _ in range(n_lines):
        print(LINE_UP, end=LINE_CLEAR)


def collect_domains(domains: tuple, src_dir: Path) -> list[Path]:
    domain_paths = []
    for domain in Path(src_dir).iterdir():
        if domain.is_dir() and domain.exists() and not domain.name.startswith("."):
            if domains[0] == "all" or domain.name in domains:
                domain_paths.append(domain)
    return domain_paths
