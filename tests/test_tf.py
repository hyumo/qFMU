import pathlib
import json
import uuid
import random
import numpy as np

import pytest
from click.testing import CliRunner

from qfmu.cli import cli

class TestTransferFunction:

    nn = random.randint(1, 20)
    nd = nn + 1

    num = np.random.rand(nn)
    den = np.random.rand(nd)

    @pytest.mark.parametrize(
        "num, den, x0, u0",
        [
            (num, den, None, None),
            (num, den, None, 1.0),
            (num, den, np.zeros(nd-1), 1.0),
        ],
    )
    def test_cli_tf(self, num, den, x0, u0):
        
        runner = CliRunner()
        with runner.isolated_filesystem() as td:
            filename = f"{td}/{uuid.uuid4()}.fmu"
            result = runner.invoke(
                cli,
                [
                    "tf",
                    "--num",
                    json.dumps(num.tolist()),
                    "--den",
                    json.dumps(den.tolist()),
                    "--dt",
                    "0.001",
                    "--output",
                    f"{filename}",
                ]
                + (["--x0", json.dumps(x0.tolist())] if x0 is not None else [])
                + (["--u0", str(u0)] if u0 is not None else [])
            )

            assert result.exit_code == 0
            assert pathlib.Path(filename).exists()