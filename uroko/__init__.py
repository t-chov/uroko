from typing import Callable, Dict, Iterator, List

from numpy import log


def min_max_scale(
    datapoints: List[Dict],
    value_keys: List[str],
    normalized_value_keys: List[str] = ["normalized_value"],
    v_min: float = 0.0,
    v_max: float = 1.0
) -> Iterator[Dict]:
    yield from min_max_scale_with_closure(
        datapoints=datapoints,
        value_keys=value_keys,
        normalized_value_keys=normalized_value_keys,
        f=lambda v: v,
        v_min=v_min,
        v_max=v_max
    )

def min_max_log_scale(
    datapoints: List[Dict],
    value_keys: List[str],
    normalized_value_keys: List[str] = ["normalized_value"],
    v_min: float = 0.0,
    v_max: float = 1.0
) -> Iterator[Dict]:
    yield from min_max_scale_with_closure(
        datapoints=datapoints,
        value_keys=value_keys,
        normalized_value_keys=normalized_value_keys,
        f=lambda v: log(v + 1),
        v_min=v_min,
        v_max=v_max
    )


def min_max_scale_with_closure(
    datapoints: List[Dict],
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

    min_max_list = [
        (f(min(d[vkey] for d in datapoints)), f(max(d[vkey] for d in datapoints)))
        for vkey in value_keys
    ]

    calc_std = lambda v, minv, maxv: (f(v) - minv) / (maxv - minv)
    for datapoint in datapoints:
        for i, (vkey, nvkey) in enumerate(zip(value_keys, normalized_value_keys)):
            rawv = datapoint[vkey]
            minv = min_max_list[i][0]
            maxv = min_max_list[i][1]
            datapoint[nvkey] = calc_std(rawv, minv, maxv) * (v_max - v_min) + v_min
        yield datapoint
