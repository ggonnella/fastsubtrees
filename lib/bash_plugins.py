import sh
import imp
from pathlib import Path

def _get_constant(filename, cname):
  return sh.bash("-c", f". {filename}; echo -e ${cname}").rstrip()

def bash(filename):
  modulename=Path(filename).stem
  m=imp.new_module(modulename)
  def _compute(unitid, **kwargs):
    kwargs_str=" ".join([f"{k}={v}" for k, v in kwargs.items()])
    retvals = sh.bash("-c", f". {filename}; compute {unitid} {kwargs_str}").\
               rstrip().split("\n", 1)
    if len(retvals) == 1:
      retvals.append("")
    return (retvals[0].split("\t"), retvals[1].split("\n"))
  for cname in ["ID", "VERSION", "INPUT", "METHOD", "IMPLEMENTATION",
                "REQ_SOFTWARE", "REQ_HARDWARE", "ADVICE"]:
    setattr(m, cname, _get_constant(filename, cname))
  m.OUTPUT = _get_constant(filename, "{OUTPUT[@]}").split(" ")
  m.PARAMETERS=[e.split("\t") for e in \
                _get_constant(filename, "{PARAMETERS[@]}").split("\n")]
  m.compute = _compute
  m.__lang__ = "bash"
  return m
