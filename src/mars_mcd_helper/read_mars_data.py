"""Functions to parse data in the rather bespoke format used by the MCD."""
from pathlib import Path
from typing import List, Union
from datetime import datetime
from collections import namedtuple
import numpy as np
import re


def parse_number(num: str) -> Union[float, int, None]:
    """
    Parse a number into the best representation. Return None if not possible.

    Args:
        num (str): number to parse.

    Returns:
        (float or int or None): parsed number.

    """
    if num == "----":
        return None
    if "." in num:
        return float(num)
    try:
        return int(num)
    except ValueError:
        return float(num)


def parse_header(lines: List[str]) -> dict:
    """Parse header.

    Args:
        lines (List[str]): lines to parse.

    Returns:
        Dict representing extracted data.
    """
    # written to be readable by people beginning python, so rather verbose.
    data = {}
    match = re.search("MCD_(.+) with (.+).", lines[0])
    if match:
        data["mcd_version"] = match.group(1)
        data["model"] = match.group(2)
    match = re.search("Ls (.+). Altitude (.+) ALS Local time (.+)", lines[1])
    if match:
        data["ls"] = match.group(1)
        data["altitude"] = match.group(2)
        data["local_time"] = match.group(3).strip()
    assert "-" * 6 in lines[2]
    match = re.search("Column 1 is (.+)", lines[3])
    if match:
        data["column_1"] = match.group(1)

    match = re.search(r"Columns 2\+ are (.+)", lines[4])
    if match:
        data["variable"] = match.group(1)

    match = re.search("Line 1 is (.+)", lines[5])
    if match:
        data["keys"] = match.group(1)
    assert "-" * 6 in lines[6]
    match = re.search("Retrieved on: (.+)", lines[7])
    if match:
        data["retrieval_date"] = datetime.fromisoformat(match.group(1))
    return data


DataTable = namedtuple("DataTable", ["data", "xlabels", "ylabels"])


def parse_body(body: List[str]) -> "DataTable":
    """
    Parse body of data from the MCD.

    Args:
        body (List[str]): lines to parse.

    Returns:
        (DataTable): The parsed data.
    """
    # here we use the map (/reduce, but here we don't reduce) paradigm
    # to show how sometimes functional programming is a *lot* simpler
    # than writing the loops out by hand.

    # map applies a function (here an anonymous function decared with lambda)
    # over an iterable

    # numpy has it's own map/reduce fns which are implemented in C
    # and can be a lot faster than python's.

    body = map(lambda row: " ".join(row.strip().split()), body)
    body = list(body)
    xlabels = body[0].split("||")[1].strip().split(" ")
    body = body[2:]
    xlabels = map(parse_number, xlabels)
    ylabels = map(lambda row: row.split("||")[0].strip(), body)
    ylabels = map(parse_number, ylabels)
    data = map(lambda row: row.split("||")[1].strip().split(" "), body)
    data = np.array(list(data))
    return DataTable(data, list(xlabels), list(ylabels))


def read_ascii_data(dataf: Path) -> dict:
    """
    Parse a file downloaded from the MCD.

    Args:
        dataf (Path): The file to pass.

    Returns:
        (dict): The data.

    """
    sections = {}
    with dataf.open() as f:
        row = f.readline()
        while True:
            if not row:
                break
            while "#" * 8 not in row:  # start header section
                row = f.readline()
            row = f.readline()  # skip ###### row
            header = []
            while "#" * 8 not in row:
                header.append(row)
                row = f.readline()
            header = parse_header(header)

            # parse body
            body = []
            row = f.readline()
            while row and "#" * 8 not in row:  # start header section
                body.append(row)
                row = f.readline()
            body = parse_body(body)
            header["data"] = body
            sections[header["variable"]] = header
    return sections
