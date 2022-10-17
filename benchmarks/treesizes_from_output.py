#!/usr/bin/env python3
"""
Create a table with tree sizes, number of nodes with attributes
and number of attribute values from the stderr output of
benchmarks_attrs.sh

Usage:
  ./treesizes_from_logs.py <captured_output>

Arguments:
  captured_output  The stderr output of benchmarks_attrs.sh

"""

from docopt import docopt
import re

# Example output of benchmarks_attrs.sh
"""
Step query-genome_size from node 83333, iteration 0...
2022-10-17 11:03:37 INFO: Number of nodes with attribute 'genome_size': 1
2022-10-17 11:03:37 INFO: Number of values of attribute 'genome_size': 9
2022-10-17 11:03:37 INFO: Number of nodes in subtree: 1
"""

def main(args):
  re1 = re.compile(r"Step query-.* from node (\d+),")
  re2 = re.compile(r"Number of nodes with attribute '.*': (\d+)")
  re3 = re.compile(r"Number of values of attribute '.*': (\d+)")
  re4 = re.compile(r"Number of nodes in subtree: (\d+)")
  with open(args["<captured_output>"]) as f:
    rootnode = None
    subtree_size = None
    nodes_with_attrs = None
    attr_values = None
    skip_output = set()
    for line in f:
      m = re1.search(line)
      if m:
        rootnode = m.group(1)
      else:
        m = re2.search(line)
        if m:
          nodes_with_attrs = m.group(1)
        else:
          m = re3.search(line)
          if m:
            attr_values = m.group(1)
          else:
            m = re4.search(line)
            if m:
              subtree_size = m.group(1)
              if rootnode not in skip_output:
                print(f"{rootnode}\t{subtree_size}\t"+\
                      f"{nodes_with_attrs}\t{attr_values}")
              skip_output.add(rootnode)

if __name__ == "__main__":
  args = docopt(__doc__)
  main(args)
