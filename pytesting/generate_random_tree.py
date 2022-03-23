#!/usr/bin/env python3

"""
Generate a tree with n nodes and a random topology.
The root of the node is labeled with 1.
The other tree nodes are labeled with integers from 2 to n.

Output:
  TSV file, with:
  - a line for the root containing:         root_id  <TAB> root_id
  - a line for each other node containing:  child_id <TAB> parent_id

Usage:
  ./generate_random_tree.py <n>

"""
from docopt import docopt
import sys
import random

def main(args):
  n = int(args["<n>"])
  if n < 1:
    sys.stderr.write("Error: n must be an integer > 0\n")
    exit(1)
  print(f"1\t1")
  for i in range(1, n):
    parent = random.randint(1, i)
    child = i+1
    print(f"{child}\t{parent}")

if __name__ == "__main__":
  arguments = docopt(__doc__, version="1.0")
  main(arguments)