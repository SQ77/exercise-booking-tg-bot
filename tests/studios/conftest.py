import inspect
import pytest
from pathlib import Path

@pytest.fixture
def load_html():
  """
  Fixture to load a HTML file from the "example_html_responses" directory
  located next to the test file calling this fixture.

  Args:
    - filename (str): Name of the HTML file to load.
      e.g. Loads "tests/studios/ally/example_html_responses/{filename}" if called from "tests/studios/ally/test_ally.py"

  Returns:
    - Callable[[str], str]: Function that returns the contents of the specified HTML file as a string.
  """
  def _load(filename: str) -> str:
    # Determine the test file calling this function
    try:
      test_file = Path(inspect.stack()[1].filename)
    except IndexError:
      raise RuntimeError("Failed to resolve test file path for load_html fixture.")

    html_path = test_file.parent / "example_html_responses" / filename
    if not html_path.exists():
      raise FileNotFoundError(f"HTML file not found: {html_path}")

    return html_path.read_text(encoding="utf-8")

  return _load
