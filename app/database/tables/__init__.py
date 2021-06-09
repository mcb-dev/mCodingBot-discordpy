from os.path import isfile, join
from os import listdir
from typing import List


def read_close(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


tables_dir: str = "app/database/tables"
filenames: List[str] = [
    join(tables_dir, f)
    for f in listdir(tables_dir)
    if isfile(join(tables_dir, f))
    and f.endswith(".sql")
]
ALL_TABLES: List[str] = [read_close(f) for f in filenames]
