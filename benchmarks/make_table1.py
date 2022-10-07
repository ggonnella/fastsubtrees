#!/usr/bin/env python3
"""
Create Table 1 of the paper from the benchmark results

The table compares the results of the benchmarks of extracting subtrees
using SQL vs using the fastsubtrees library.

It shows the ID of the root node of the subtree, the size of the subtree,
the average CPU and real time to extract the subtree using SQL and fastsubtrees
and the memory peaks of the two methods.

Usage:
  ./make_table1.py <benchmarks_sql> <benchmarks_fastsubtrees> <subtree_sizes>
"""

from docopt import docopt
from collections import defaultdict

headers = {
    'subtree_id': 'Subtree root ID',
    'subtree_size': 'Subtree size',
    'sql_cpu_time': 'SQL CPU time (s)',
    'sql_real_time': 'SQL real time (s)',
    'sql_memory_peak': 'SQL memory peak (MB)',
    'fastsubtrees_cpu_time': 'fastsubtrees CPU time (s)',
    'fastsubtrees_real_time': 'fastsubtrees real time (s)',
    'fastsubtrees_memory_peak': 'fastsubtrees memory peak (MB)',
}

order = ['subtree_size', 'sql_cpu_time', 'fastsubtrees_cpu_time',\
         'sql_real_time', 'fastsubtrees_real_time', 'sql_memory_peak',\
         'fastsubtrees_memory_peak']

def read_benchmarks(results, filename,
                    key_cpu_time, key_real_time, key_memory_peak):
  with open(filename) as f:
    # example line of the benchmark results:
    # extract	511145	0	0.15	0.01	1.51	34736
    for line in f:
      fields = line.rstrip().split('\t')
      if fields[0] == 'extract':
        subtree_id = fields[1]
        if results.get(subtree_id) is None:
          results[subtree_id] = defaultdict(list)
        results[subtree_id][key_cpu_time].append(\
            float(fields[3]) + float(fields[4]))
        results[subtree_id][key_real_time].append(float(fields[5]))
        results[subtree_id][key_memory_peak].append(int(fields[6]))
    # compute means
    for subtree_id in results:
      for key in [key_cpu_time, key_real_time, key_memory_peak]:
        results[subtree_id][key] = \
            sum(results[subtree_id][key]) / len(results[subtree_id][key])
    # format floats
    for subtree_id in results:
      for key in [key_cpu_time, key_real_time]:
        results[subtree_id][key] = '{:.2f}'.format(results[subtree_id][key])
      results[subtree_id][key_memory_peak] = \
          '{:.1f}'.format(results[subtree_id][key_memory_peak] / 1024)

def main(args):
  results = {}
  read_benchmarks(results, args['<benchmarks_sql>'], 'sql_cpu_time', \
      'sql_real_time', 'sql_memory_peak')
  read_benchmarks(results, args['<benchmarks_fastsubtrees>'], \
      'fastsubtrees_cpu_time', 'fastsubtrees_real_time', \
      'fastsubtrees_memory_peak')
  lines_order = []
  with open(args['<subtree_sizes>']) as f:
    for line in f:
      fields = line.rstrip().split('\t')
      subtree_id = fields[0]
      lines_order.append(subtree_id)
      subtree_size = fields[1]
      results[subtree_id]['subtree_size'] = subtree_size
  print('|' + ' | '.join([headers["subtree_id"]] + \
                         [headers[x] for x in order]) + '|')
  print('|-'*(len(order)+1) + '|')
  for subtree_id in lines_order:
    print('|' + ' | '.join([subtree_id] + \
                           [str(results[subtree_id][x]) for x in order]) + '|')

if __name__ == "__main__":
  args = docopt(__doc__)
  main(args)
