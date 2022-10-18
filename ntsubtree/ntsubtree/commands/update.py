#!/usr/bin/env python3
"""
Update the tree with new data from NCBI, if available

Usage:
  ntsubtree update [options]

Further options:
  -f, --force      force update even if the tree is up-to-date
  -q, --quiet      disable log messages
  -d, --debug      print debug information
  -h, --help       show this help message and exit
  -V, --version    show program's version number and exit
"""

from ntsubtree import update

def main(args):
  ntsubtree.update(force_download=args["--force"])
