#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest
import os
from pathlib import Path

@pytest.fixture
def testout():
  return lambda fn: Path(__file__).parent / 'output' / fn


