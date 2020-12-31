#!/usr/bin/python3

import ast
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

# Containing product codes and descriptions (fixed for this application)
PROD_PATH = "data/products.txt"

# Preload dictionary of recognized products from product store (text file)
with open(PROD_PATH) as f:
    data = f.read()
    prod_categories = ast.literal_eval(data)


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


def parse_line(line):
    """ Separate out product code, subtype, barcode. Validate. """
    code = line[:4]
    subtype = line[4:10]
    id = line[10:]

    if code not in prod_categories.keys():
        raise ValueError(f"Invalid product code {code}")

    return code, subtype, id


def process_file(file, productcode):
    """Main file processing function.

    This function reads the first line and parses/validates date and name.
    A shopping dict is created listing unique IDs for all product codes.
    If a product code is specified, all subtypes for it are collected.
    """
    header = file.readline().strip()
    if re.match(DATEFORMAT, header[:8]):
        date = datetime.datetime.strptime(header[:8], "%m%d%Y").date()
    else:
        raise ValueError(f"Invalid date (ddmmyyy) {header[:8]}")
    name = header[8:]

    shopping = {}
    subtypes = []
    for line in file:
        line = line.strip()
        if len(line) != 30:
            raise ValueError(f"Invalid barcode length {line}")

        code, subtype, id = parse_line(line)
        if code in shopping:
            shopping[code].append(id)
        else:
            shopping[code] = [id]

        if productcode is not None and productcode.upper() == code:
            subtypes.append(subtype)

    return name, date, shopping, subtypes


def count_shopping(shopping):
    """ Traverse shopping dictionary to find most common items + subtype. """
    count = 0
    max = 0
    for key, value in shopping.items():
        count += len(value)
        if len(value) > max:
            max = len(value)

    return count, max


@click.group()
def cli():
    pass  # Entry Point


@cli.command()
@click.option("--filename", "-f", default="data/CustomerG.txt")
@click.option("--productcode", "-p", default=None)
@click.option("--uniqueids", "-i", is_flag=True, default=False)
def process(filename, productcode, uniqueids):
    """Process an input file generated by a sale.

    This function ensured that the specified input exists, and then calls
    the file processing function. Outputs are displayed on the console.
    """
    path = get_path(filename)
    with open(path, "r") as f:
        name, date, shopping, subtypes = process_file(f, productcode)

    count, max = count_shopping(shopping)

    print(f"Customer Name: {name}")
    print(f"Purchase Date: {date}")
    print(f"Number of items purchased: {count}")

    most_common = []
    for key, value in shopping.items():
        if uniqueids:
            print(f"Item code {key}: purchased {len(value)} item(s)({value})")
        if len(value) == max:
            most_common.append(key)

    print(
        f"The most common product type(s) is(are): {most_common}"
        f" with {max} items in the purchase"
    )

    if productcode is not None:
        print(f"Subtype(s) for {productcode.upper()}: {subtypes}")


@cli.command()
@click.option("--productcode", "-p", default=None)
@click.option("--description", "-d", default=None)
def add(productcode, description):
    """Add a new product code to list of products.

    This function adds a new product code and description to the list
    of products in the product store (in this case, a text file).
    """
    if productcode is None:
        raise ValueError("No product code specified")
    if len(productcode) != 4:
        raise ValueError(
            f"Invalid product code {productcode.upper()}(must be 4 characters)"
        )
    if productcode.upper() in prod_categories.keys():
        raise ValueError(f"Duplicate product code {productcode.upper()}")
    if description is None:
        raise ValueError(
            "No description for product code {productcode.upper()} specified"
        )

    print(f"Adding {productcode.upper()} ({description}) to product store.")
    prod_categories[productcode.upper()] = description

    with open(PROD_PATH, "w+") as f:
        f.write(str(prod_categories))


if __name__ == "__main__":
    """ Call the process command. """
    cli()
