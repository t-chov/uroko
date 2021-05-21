import csv
import sys
from typing import Iterable, Optional, TextIO

from click import Choice, File, argument, command, option, version_option
from uroko import FUNC_ASIS, FUNC_LOG, FUNC_SQRT, min_max_scale_with_closure

FUNCTIONS = {
    'log': FUNC_LOG,
    'sqrt': FUNC_SQRT,
}

@command()
@version_option(version="0.2.2")
@argument('input', type=File('r', lazy=True), default=sys.stdin)
@argument('output', type=File('w', lazy=True), default=sys.stdout)
@option(
    '-c', '--columns',
    help='columns to scale',
    type=str,
    multiple=True
)
@option(
    '-a', '--apply',
    type=Choice(['log', 'sqrt']),
    default=None,
    help='apply whith calculation for scaling'
)
@option(
    '--csv',
    'delimiter',
    flag_value=",",
    help='load as csv',
    default=True
)
@option(
    '--tsv',
    'delimiter',
    flag_value="\t",
    help='load as tsv'
)
def main(
    input: TextIO,
    output: TextIO,
    columns: Iterable[str],
    apply: Optional[str],
    delimiter: str
) -> None:
    columns = list(columns)
    reader = csv.DictReader(input, delimiter=delimiter)
    writer = csv.DictWriter(
        output,
        delimiter=delimiter,
        fieldnames=reader.fieldnames
    )
    func = FUNCTIONS[apply] if apply else FUNC_ASIS
    scaled = min_max_scale_with_closure(
        reader,
        value_keys=columns,
        normalized_value_keys=columns,
        f=func
    )
    writer.writeheader()
    writer.writerows(scaled)
