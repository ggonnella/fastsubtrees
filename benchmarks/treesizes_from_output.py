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
2022-10-07 09:31:18 INFO: Subtree of node 2 has size 535205
2022-10-07 09:31:19 INFO: Number of nodes with attributes: 10043
2022-10-07 09:31:19 INFO: Number of attribute values: 27515
"""

def main(args):
  re1 = re.compile(r"Subtree of node (\d+) has size (\d+)")
  re2 = re.compile(r"Number of nodes with attributes: (\d+)")
  re3 = re.compile(r"Number of attribute values: (\d+)")
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
        subtree_size = m.group(2)
      else:
        m = re2.search(line)
        if m:
          nodes_with_attrs = m.group(1)
        else:
          m = re3.search(line)
          if m:
            attr_values = m.group(1)
            if rootnode not in skip_output:
              print(f"{rootnode}\t{subtree_size}\t"+\
                    f"{nodes_with_attrs}\t{attr_values}")
            skip_output.add(rootnode)

if __name__ == "__main__":
  args = docopt(__doc__)
  main(args)
