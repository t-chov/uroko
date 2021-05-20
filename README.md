# uroko

[![PyPI version](https://badge.fury.io/py/uroko.svg)](https://pypi.org/project/uroko/)
[![CircleCI](https://circleci.com/gh/t-chov/uroko.svg?style=svg)](https://app.circleci.com/pipelines/github/t-chov/uroko)
[![Codecov](https://codecov.io/gh/t-chov/uroko/branch/main/graph/badge.svg)](https://app.codecov.io/gh/t-chov/uroko)

Data scaling tool for CSV/TSV

"uroko" means scale in Japanese.

Input CSV/TSV data, output min-max scaled data with some functions.

## Usage

```
Usage: uroko-cli [OPTIONS] [INPUT] [OUTPUT]

Options:
  --version               Show the version and exit.
  -c, --columns TEXT      columns to scale
  -a, --apply [log|sqrt]  apply whith calculation for scaling
  --csv                   load as csv
  --tsv                   load as tsv
  --help                  Show this message and exit.
```

## Example

### Plain

```
$ echo """name,score
Sato,100
Kimura,50
Suzuki,80
""" | uroko-cli -c score
name,score
Sato,1.0
Kimura,0.0
Suzuki,0.6
```

### Use log scale

```
echo """name      value
kyoto   10000
gifu    100
gumma   1
""" | uroko-cli -c value -a log --tsv
name    value
kyoto   1.0
gifu    0.4604718013624446
gumma   0.0
```
