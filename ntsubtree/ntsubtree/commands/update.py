#!/usr/bin/env python3
"""
Update the tree with new data from NCBI, if available

Usage:
  ntsubtree update [options]

Further options:
  -c, --cleanup    cleanup all files and recostruct from scratch
                   (it also eliminates all existing attribute data!)
  -f, --force      force downlading and updating even if the tree is up-to-date
  -r, --rebuild    force rebuilding tree (implicing in --force)
  -q, --quiet      disable log messages
  -d, --debug      print debug information
  -h, --help       show this help message and exit
  -V, --version    show program's version number and exit
"""

from ntsubtree import update, setup

def main(args):
  if args["--cleanup"]:
    setup()
  else:
    update(force_download=args["--force"],
           force_construct=args["--rebuild"])
