from pathlib import Path
import shutil

import pytest

@pytest.fixture(scope="session")
def test_data_session(tmp_path_factory):
    src = Path(__file__).parent / "data"
    dst = tmp_path_factory.mktemp("session_data")

    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)

    return dst