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

@pytest.fixture
def test_data(tmp_path):
    src = Path(__file__).parent / "data"
    for item in src.iterdir():
        target = tmp_path / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
    return tmp_path

@pytest.fixture
def isolated_project(tmp_path):
    """Copy the minimal working project subset to a temp directory."""
    root = Path(__file__).parent.parent  # assume tests/ is one level down
    paths_to_copy = [
        "Makefile",
        "stitchjob",
        "letter/example.md",
        "resume/example.xml"
    ]

    for rel_path in paths_to_copy:
        src = root / rel_path
        dst = tmp_path / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    return tmp_path

def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="Run tests marked as slow"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="Skipped by default; use --runslow to include")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)