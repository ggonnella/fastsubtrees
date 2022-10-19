#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
from pathlib import Path

@pytest.fixture
def testout():
  return lambda fn: Path(__file__).parent / 'output' / fn

@pytest.fixture
def testdata_dir():
  return Path(__file__).parent / 'testdata'

@pytest.fixture
def script():
  return lambda fn: Path(__file__).parent.parent / 'bin' / fn

