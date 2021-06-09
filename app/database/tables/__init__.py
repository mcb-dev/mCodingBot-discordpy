from os.path import isfile, join
from os import listdir


def read_close(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()


tables_dir = "app/database/tables"
filenames = [
    join(tables_dir, f)
    for f in listdir(tables_dir)
    if isfile(join(tables_dir, f))
    and f.endswith(".sql")
]
ALL_TABLES = [
    read_close(f)
    for f in filenames
]
