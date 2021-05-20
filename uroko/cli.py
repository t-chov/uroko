import csv
import sys
from typing import Iterable, TextIO

from click import File, argument, command, option, version_option

from uroko import min_max_scale


@command()
@version_option(version="0.1.0")
@argument('input', type=File('r', lazy=True), default=sys.stdin)
@argument('output', type=File('w', lazy=True), default=sys.stdout)
@option(
    '-c', '--columns',
    help='columns to scale',
    type=str,
    multiple=True
)
@option('--csv', 'delimiter', flag_value=",", default=True)
@option('--tsv', 'delimiter', flag_value="\t")
def main(
    input: TextIO,
    output: TextIO,
    columns: Iterable[str],
    delimiter: str
) -> None:
    columns = list(columns)
    reader = csv.DictReader(input, delimiter=delimiter)
    writer = csv.DictWriter(
        output,
        delimiter=delimiter,
        fieldnames=reader.fieldnames
    )
    scaled = min_max_scale(
        reader,
        value_keys=columns,
        normalized_value_keys=columns
    )
    writer.writeheader()
    writer.writerows(scaled)
