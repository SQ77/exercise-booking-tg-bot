import inspect
from pathlib import Path

import pytest


@pytest.fixture
def load_response_file():
    """
    Fixture to load a file from the "example_responses" directory located next to the
    test file calling this fixture.

    Args:
      - filename (str): Name of the file to load.
        e.g. Loads "tests/studios/ally/example_responses/{filename}" if called from "tests/studios/ally/test_ally.py"

    Returns:
      - Callable[[str], str]: Function that returns the contents of the specified file as a string.

    """

    def _load(filename: str) -> str:
        # Determine the test file calling this function
        try:
            test_file = Path(inspect.stack()[1].filename)
        except IndexError:
            raise RuntimeError("Failed to resolve test file path for load_response_file fixture.")

        path = test_file.parent / "example_responses" / filename
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        return path.read_text(encoding="utf-8")

    return _load
