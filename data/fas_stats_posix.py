#!/usr/bin/env python3
"""
Compute basic sequence statistics using Posix command line tools

Usage:
  ./fas_stats_posix.py [options] <filename>

Arguments:
  <filename>  Input file (Fasta format, by default: gzipped)

Options:
  --uncompressed   Input file is not compressed (default: gzipped)
  -h --help        Show this screen.
  --version        Show version.
"""

from docopt import docopt
import sh

def compute(filename, uncompressed):
  countchars = sh.wc.bake(c=True)
  gc_only = sh.tr.bake("-dc", "[GCgc]", _piped=True)
  non_space = sh.tr.bake(d="[:space:]", _piped=True)
  vgrep = sh.grep.bake(_piped=True, v=True)
  unzipped = sh.zcat.bake(_piped=True)
  if uncompressed:
    genomelen = int(countchars(non_space(vgrep("^>", filename))))
    gclen = int(countchars(gc_only(vgrep("^>", filename))))
  else:
    genomelen = int(countchars(non_space(vgrep(unzipped(filename), "^>"))))
    gclen = int(countchars(gc_only(vgrep(unzipped(filename), "^>"))))
  return (genomelen, gclen/genomelen)

def main(args):
  genomelen, gc = compute(args["<filename>"], args["--uncompressed"])
  print("{}\t{}\t{:.2f}".format(args["<filename>"], genomelen, gc))

if __name__ == "__main__":
  args = docopt(__doc__, version="0.1")
  main(args)
