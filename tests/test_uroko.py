from pytest import raises
from uroko import min_max_log_scale, min_max_scale


def test_min_max_scale_value_error():
    with raises(RuntimeError) as err:
        _ = list(min_max_scale([{}], ("foo", "bar")))

    assert 'value_keys and normalized_value_keys must have same length' in str(err)


def test_min_max_scale():
    input = [
        {
            "name": "Sato",
            "age": 20,
            "height": 175,
        },
        {
            "name": "Suzuki",
            "age": 44,
            "height": 160,
        },
        {
            "name": "Yoshida",
            "age": 50,
            "height": 190,
        },
    ]
    expected = [
        {
            "name": "Sato",
            "age": 20,
            "height": 0.5,
            "nage": 0.0,
        },
        {
            "name": "Suzuki",
            "age": 44,
            "height": 0.0,
            "nage": 0.8,
        },
        {
            "name": "Yoshida",
            "age": 50,
            "height": 1.0,
            "nage": 1.0,
        },
    ]
    assert list(min_max_scale(input, ["age", "height"], ["nage", "height"])) == expected


def test_min_max_log_scale():
    input = [
        {
            "name": "Kyoto",
            "point": 10000,
        },
        {
            "name": "Okayama",
            "point": 10,
        },
        {
            "name": "Gumma",
            "point": 1,
        },
    ]
    actual = list(min_max_log_scale(input, ["point"], ["point"], 1.0, 2.0))
    assert actual[0]["point"] == 2.0
    assert round(actual[1]["point"], 5) == 1.20015
    assert actual[2]["point"] == 1.0
