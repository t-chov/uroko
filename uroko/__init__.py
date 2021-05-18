from typing import Dict, Iterator, List, Tuple


def min_max_scale(
    datapoints: List[Dict],
    value_keys: Tuple[str],
    normalized_value_keys: Tuple[str] = tuple("normalized_value"),
    v_min: float = 0.0,
    v_max: float = 1.0
) -> Iterator[Dict]:
    if len(value_keys) != len(normalized_value_keys):
        msg = 'value_keys and normalized_value_keys must have same length'
        detail = f'v: `{"/".join(value_keys)}` n:`{"/".join(normalized_value_keys)}`'
        raise RuntimeError(f'{msg}({detail})')

    min_max_list = [
        (min(d[vkey] for d in datapoints), max(d[vkey] for d in datapoints))
        for vkey in value_keys
    ]

    calc_std = lambda v, minv, maxv: (v - minv) / (maxv - minv)
    for datapoint in datapoints:
        for i, (vkey, nvkey) in enumerate(zip(value_keys, normalized_value_keys)):
            rawv = datapoint[vkey]
            minv = min_max_list[i][0]
            maxv = min_max_list[i][1]
            datapoint[nvkey] = calc_std(rawv, minv, maxv) * (v_max - v_min) + v_min
        yield datapoint
