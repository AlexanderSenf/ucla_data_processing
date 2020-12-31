#!/usr/bin/python3

import datetime
import errno
import os
import pathlib
import re

import click

# Courtesy of https://stackoverflow.com/questions/15491894/
#                     regex-to-validate-date-format-dd-mm-yyyy
DATEFORMAT = (
    "^(((0[13-9]|1[012])[-/]?(0[1-9]|[12][0-9]|30)|(0[13578]|1[02])"
    "[-/]?31|02[-/]?(0[1-9]|1[0-9]|2[0-8]))[-/]?[0-9]{4}|02[-/]"
    "?29[-/]?([0-9]{2}(([2468][048]|[02468][48])|[13579][26])|"
    "([13579][26]|[02468][048]|0[0-9]|1[0-6])00))$"
)


def get_path(filename):
    """Get a file system path from user input.

    If the specified input file exists as a relative path, it is used.
    Otherwise it ie expanded to a full system path, and as a final step the
    '/data/' directory is prepended (in case the input is in the /data dir).
    """
    p = pathlib.Path(filename)
    if p.exists():
        return p
    elif (pathlib.Path.cwd() / filename).exists():
        return pathlib.Path.cwd() / filename
    elif (pathlib.Path.cwd() / "data" / filename).exists():
        return pathlib.Path.cwd() / "data" / filename
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), p)


def process_file(file):
    """Main file processing function.

    This function reads the first line and parses/validates date and name.
    Subsequenct lines are simply validated and counted, to provide item count.
    """
    header = file.readline().strip()
    if re.match(DATEFORMAT, header[:8]):
        date = datetime.datetime.strptime(header[:8], "%m%d%Y").date()
    else:
        raise ValueError(f"Invalid date (ddmmyyy) {header[:8]}")
    name = header[8:]

    count = 0
    for line in file:
        line = line.strip()
        if len(line) != 30:
            raise ValueError(f"Invalid barcode length {line}")
        count += 1

    return name, date, count


@click.command()
@click.option("--filename", "-f", default="data/CustomerG.txt")
def process(filename):
    """Click command with optional filename as input parameter.

    This function ensured that the specified input exists, and then calls
    the file processing function. Outputs are displayed on the console.
    """
    path = get_path(filename)
    with open(path, "r") as f:
        name, date, count = process_file(f)

    print(f"Customer Name: {name}")
    print(f"Purchase Date: {date}")
    print(f"Number of items purchased: {count}")


if __name__ == "__main__":
    """ Call the process command. """
    process()
