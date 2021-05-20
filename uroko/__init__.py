from itertools import tee
from typing import Callable, Dict, Iterable, Iterator, List

from numpy import log, sqrt

FUNC_ASIS = lambda x: x
FUNC_LOG = lambda x: log(x + 1)
FUNC_SQRT = lambda x: sqrt(x)

def min_max_scale(
    datapoints: Iterable[Dict],
    value_keys: List[str],
    normalized_value_keys: List[str] = ["normalized_value"],
    v_min: float = 0.0,
    v_max: float = 1.0
) -> Iterator[Dict]:
    yield from min_max_scale_with_closure(
        datapoints=datapoints,
        value_keys=value_keys,
        normalized_value_keys=normalized_value_keys,
        f=FUNC_ASIS,
        v_min=v_min,
        v_max=v_max
    )

def min_max_log_scale(
    datapoints: Iterable[Dict],
    value_keys: List[str],
    normalized_value_keys: List[str] = ["normalized_value"],
    v_min: float = 0.0,
    v_max: float = 1.0
) -> Iterator[Dict]:
    yield from min_max_scale_with_closure(
        datapoints=datapoints,
        value_keys=value_keys,
        normalized_value_keys=normalized_value_keys,
        f=FUNC_LOG,
        v_min=v_min,
        v_max=v_max
    )


def min_max_scale_with_closure(
    datapoints: Iterable[Dict],
    value_keys: List[str],
    normalized_value_keys: List[str] = ["normalized_value"],
    f: Callable[[float], float] = lambda v: v,
    v_min: float = 0.0,
    v_max: float = 1.0
) -> Iterator[Dict]:
    if len(value_keys) != len(normalized_value_keys):
        msg = 'value_keys and normalized_value_keys must have same length'
        detail = f'v: `{"/".join(value_keys)}` n:`{"/".join(normalized_value_keys)}`'
        raise RuntimeError(f'{msg}({detail})')

    # to use huge datapoints, use iterators
    rows, predata = tee(datapoints)
    values = []
    for vkey in value_keys:
        values.append([float(d[vkey]) for d in predata])
        _, predata = tee(datapoints)
    min_max_list = [
        (f(min(values[i])), f(max(values[i]))) for i, _ in enumerate(value_keys)
    ]

    calc_std = lambda v, minv, maxv: (f(v) - minv) / (maxv - minv)
    for datapoint in rows:
        for i, (vkey, nvkey) in enumerate(zip(value_keys, normalized_value_keys)):
            rawv = float(datapoint[vkey])
            minv = min_max_list[i][0]
            maxv = min_max_list[i][1]
            datapoint[nvkey] = calc_std(rawv, minv, maxv) * (v_max - v_min) + v_min
        yield datapoint
