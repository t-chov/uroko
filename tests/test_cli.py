from tempfile import NamedTemporaryFile
from unittest.mock import ANY

from click.testing import CliRunner
from uroko.cli import main

PKG = 'uroko.cli'


def test_main_plain(mocker):
    scale = mocker.patch(f'{PKG}.min_max_scale', return_value=[])
    with NamedTemporaryFile('w+') as input, NamedTemporaryFile('w+') as output:
        rows = (
            'name,score',
            'Sato,100',
        )
        input.write('\n'.join(rows))
        input.seek(0)
        result = CliRunner().invoke(main, [
            '-c', 'score',
            input.name,
            output.name,
        ])
        assert result.exit_code == 0

        scale.assert_called_once_with(
            ANY,
            value_keys=["score"],
            normalized_value_keys=["score"],
        )
