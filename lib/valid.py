from schema import Or, And, Use
import sys
import gzip
import yaml
import socket
import getpass

def open_maygz(fname):
  ft = open(fname, "rb")
  if ft.read(2) == b'\x1f\x8b':
    ft.close()
    return gzip.open(fname, "rt")
  else:
    ft.close()
    return open(fname)

infile_or_stdin = Or(And(None, Use(lambda v: sys.stdin)), Use(open))

maygz_or_stdin = Or(And(None, Use(lambda v: sys.stdin)),
                       Use(open_maygz))

outfile_or_stdout = Or(And(None, Use(lambda f: sys.stdout)),
                    Use(lambda f: open(f, "w")))
outfile_or_stderr = Or(And(None, Use(lambda f: sys.stderr)),
                    Use(lambda f: open(f, "w")))

outfile_or_none = Or(None, Use(lambda f: open(f, "w")))

comments = Or(And(None, Use(lambda v: "#")), str)
delimiter = Or(And(None, Use(lambda v: "\t")), And(str, len))

user = Or(str, And(None, Use(lambda n: getpass.getuser())))
system = Or(str, And(None, Use(lambda n: socket.gethostname())))
yamlfile = Or(And(None, Use(lambda n: {})),
              And(Use(open), Use(lambda fn: yaml.safe_load(fn))))

colnum = And(Use(int), lambda n: n>0)
optcolnum = Or(And(None, Use(lambda n: 1)), colnum)
