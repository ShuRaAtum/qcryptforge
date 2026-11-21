import re
from pathlib import Path

import pytest


README = Path(__file__).resolve().parents[1] / "README.md"


@pytest.mark.parametrize("example", re.findall(r"^```python\n(.*?)^```", README.read_text(), re.M | re.S))
def test_readme(example):
    if "qiskit" in example:
        pytest.importorskip("qiskit")
    exec(compile(example, str(README), "exec"), {})
