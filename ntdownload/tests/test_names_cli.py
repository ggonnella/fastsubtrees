#
# (c) 2022 Giorgio Gonnella, University of Goettingen, Germany
#
import pytest

@pytest.mark.script_launch_mode('subprocess')
def test_names(testdata_dir, script, script_runner):
  ret = script_runner.run(script('ntnames'), testdata_dir)
  assert ret.returncode == 0
  assert ret.stdout == "1\troot\n2\tBacteria\n"
