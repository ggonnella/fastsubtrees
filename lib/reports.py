import yaml
import uuid
from datetime import datetime
from lib import valid
from schema import Or

reasons = ["new_data", "new_attributes", "improve_precision"]

args_schema = {"--report": valid.outfile_or_stderr, "--user": valid.user,
          "--reason": Or(None, lambda r: r in reasons),
          "--system": valid.system, "--params": valid.yamlfile}

args_doc = """\
  --report, -r FN   computation report file (default: stderr)
  --user U          user_id for the report (default: getpass.getuser())
  --system S        system_id for the report (default: socket.gethostname())
  --reason R        reason field for the report (default: None)
  --params FNAME    YAML file with additional parameters (default: None)"""

snake_args = {"input": ["--params"], "output": ["--report"],
    "params": ["--user", "--system", "--reason"]}

class Report():

  @classmethod
  def from_args(cls, plugin, args):
    return cls(args["--report"], plugin, args["--user"], args["--system"],
               args["--reason"], args["--params"])

  def __init__(self, rfile, plugin, user, system, reason, params):
    self.rfile = rfile
    self.data = {}
    self.data["plugin_id"] = plugin.ID
    self.data["plugin_version"] = plugin.VERSION
    self.data["system_id"] = system
    self.data["user_id"] = user
    if reason:
      self.data["reason"] = reason
    if params:
      self.data["parameters"] = yaml.dump(params)
    self.data["uuid"] = uuid.uuid4().bytes
    self.data["time_start"] = str(datetime.now())
    self.n_steps = 0

  def step(self):
    self.n_steps += 1

  def finalize(self):
    self.data["time_end"] = str(datetime.now())
    self.data["n_units"] = self.n_steps
    self.data["comp_status"] = "completed"
    yaml.dump(self.data, self.rfile)
    self.rfile.flush()

  def error(self, err, unitname):
    self.data["time_end"] = str(datetime.now())
    self.data["n_units"] = self.n_steps
    self.data["comp_status"] = "aborted" if self.n_steps == 0 else "partial"
    remark = {}
    remark["error_input_unit"] = unitname
    remark["error_class"] = err.__class__.__name__
    remark["error_message"] = str(err)
    self.data["remarks"] = yaml.dump(remark)
    yaml.dump(self.data, self.rfile)
    self.rfile.flush()

