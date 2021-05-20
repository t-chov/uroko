# uroko

![PyPI version](https://badge.fury.io/py/preacher.svg)
![CircleCI](https://circleci.com/gh/t-chov/uroko.svg?style=svg)
![Codecov](https://codecov.io/gh/ymoch/preacher/branch/master/graph/badge.svg)

Data scaling tool for CSV/TSV

"uroko" means scale in Japanese.

Input CSV/TSV data, output min-max scaled data with some functions.

## Usage

```
Usage: uroko-cli [OPTIONS] [INPUT] [OUTPUT]

Options:
  --version           Show the version and exit.
  -c, --columns TEXT  columns to scale
  --help              Show this message and exit.
```

## Example

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
