import json
import glob

EXT = "attr"

def attrfilename(treefilename, attribute):
  return "{}.{}.{}".format(treefilename, attribute, EXT)

def attrfiles(treefilename):
  result = {}
  for file in glob.glob(treefilename + ".*." + EXT):
    attribute = file[len(treefilename)+1:-(len(EXT))-1]
    result[attribute] = file
  return result

def get_attribute_value(attributefile, subtree_size, position):
  with open(attributefile, 'r') as file:
    contents = file.read().splitlines()
  attribute_value_list = list()
  for i in range(position, (position + subtree_size)):
    data = json.loads(contents[i])
    attribute_value_list.append(data)
  return attribute_value_list

def get_attribute_list(tree, subtree_root, attributefile):
  treedata, position, subtree_size, subtree_parents = \
      tree.query_subtree(subtree_root)
  attribute_list = \
      get_attribute_value(attributefile, subtree_size+1, position-1)
  return attribute_list

def write_attribute_values(tree, attrvalues, outfile):
  for element_id in tree.subtree_ids(tree.root_id):
    attribute = attrvalues.get(element_id, None)
    outfile.write(json.dumps(attribute) + "\n")

def read_attribute_values(tree, fname):
  i = 0
  all_ids = tree.subtree_ids(tree.root_id)
  existing = {}
  with open(fname, "r") as f:
    for line in f:
      data = json.loads(line.rstrip())
      existing[all_ids[i]] = data
      i += 1
  return existing
