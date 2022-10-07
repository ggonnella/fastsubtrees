#!/usr/bin/env python3
"""
Create Table 2 of the paper from the benchmark results

The table shows the results of the benchmarks of extracting the attributes
of subtrees using the fastsubtrees library.

It shows the ID of the root node of the subtree, the size of the subtree,
the average CPU and real time and memory peak of the operation.

Usage:
  ./make_table2.py <benchmarks_attrs> <subtree_sizes> <attribute>
"""

from docopt import docopt
from collections import defaultdict

headers = {
    'subtree_id': 'Subtree root ID',
    'subtree_size': 'Subtree size',
    'cpu_time': 'CPU time (s)',
    'real_time': 'Real time (s)',
    'memory_peak': 'Memory peak (MB)',
    'n_nodes_with_values': 'N. nodes with values',
    'n_values': 'N. values'
}

order = ['subtree_size', 'cpu_time', 'real_time', 'memory_peak', \
         'n_nodes_with_values', 'n_values']

def read_benchmarks(results, filename, attribute,
                    key_cpu_time, key_real_time, key_memory_peak):
  with open(filename) as f:
    # example line of the benchmark results:
    # query-genome_size	511145	0	0.11	0.10	0.21	313092
    for line in f:
      fields = line.rstrip().split('\t')
      if fields[0] == f'query-{attribute}':
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
  read_benchmarks(results, args['<benchmarks_attrs>'], args['<attribute>'], \
      'cpu_time', 'real_time', 'memory_peak')
  lines_order = []
  with open(args['<subtree_sizes>']) as f:
    for line in f:
      fields = line.rstrip().split('\t')
      subtree_id = fields[0]
      lines_order.append(subtree_id)
      results[subtree_id]['subtree_size'] = fields[1]
      results[subtree_id]['n_nodes_with_values'] = fields[2]
      results[subtree_id]['n_values'] = fields[3]
  print('| ' + ' | '.join([headers["subtree_id"]] + \
                         [headers[x] for x in order]) + ' |')
  print('|-'*(len(order)+1) + '|')
  for subtree_id in lines_order:
    print('| ' + ' | '.join([subtree_id] + \
                           [str(results[subtree_id][x]) for x in order]) + ' |')

if __name__ == "__main__":
  args = docopt(__doc__)
  main(args)
