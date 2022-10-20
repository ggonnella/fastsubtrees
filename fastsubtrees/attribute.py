"""
Attribute operations for fastsubtrees.Tree objects.
"""

from collections import defaultdict
from typing import List, Union, Dict, Any
import json
import glob
from pathlib import Path
from fastsubtrees import logger, error
from fastsubtrees.ids_modules import attr_from_tabular_file

class TreeAttributes():

  ATTR_EXT = "attr"

  NONELINE = 'null\n'

  def _edit_attribute_values(self, edit_script, attrfilenames):
    for attrfilename in attrfilenames:
      with open(attrfilename, 'r') as f:
        lines = f.readlines()
      for op in edit_script:
        if op[0] == "insert":
          lines.insert(op[1]-1, self.NONELINE)
        elif op[0] == "copy":
          lines[op[2]-1] = lines[op[1]-1]
        elif op[0] == "delete":
          lines[op[1]-1] = self.NONELINE
      with open(attrfilename, 'w') as f:
        f.writelines(lines)

  @staticmethod
  def compute_attribute_filename(treefilename, attribute):
    return Path(f"{treefilename}.{attribute}.{TreeAttributes.ATTR_EXT}")

  @staticmethod
  def existing_attribute_filenames(treefilename: Union[str, Path]) \
      -> Dict[str, Path]:
    treefilename = str(treefilename)
    result = {}
    globpattern = treefilename + ".*." + TreeAttributes.ATTR_EXT
    for file in glob.glob(globpattern):
      attribute = file[len(treefilename)+1:-(len(TreeAttributes.ATTR_EXT))-1]
      result[attribute] = Path(file)
    return result

  def destroy_all_attributes(self):
    """
    Destroys all attribute values associated with the tree.
    """
    self._check_filename_set()
    for filename in self.existing_attribute_filenames(self.filename).values():
      logger.info("Removing obsolete attribute file {}".format(filename))
      filename.unlink()

  def attribute_filename(self, attribute) -> Path:
    """
    Returns the filename where the attribute values are stored.
    """
    self._check_filename_set()
    return self.compute_attribute_filename(self.filename, attribute)

  def list_attributes(self) -> List[str]:
    """
    Returns a list of the attribute names.
    """
    self._check_filename_set()
    return list(self.existing_attribute_filenames(self.filename).keys())

  def has_attribute(self, attribute):
    attrfilename = self.attribute_filename(attribute)
    return attrfilename.exists()

  def __check_has_attribute(self, attribute):
    if not self.has_attribute(attribute):
      attrfilename = self.attribute_filename(attribute)
      raise error.AttributeNotFoundError(\
          f"Attribute '{attribute}' does not exist "+\
          f"(file '{attrfilename}' does not exist)")

  def destroy_attribute(self, attribute: str):
    """
    Destroys the attribute values associated with the given attribute.
    """
    self._check_filename_set()
    self.__check_has_attribute(attribute)
    filename = self.attribute_filename(attribute)
    logger.info("Removing obsolete attribute file {}".format(filename))
    filename.unlink()

  def subtree_attribute_data(self, subtree_root, attribute):
    self._check_filename_set()
    self.__check_has_attribute(attribute)
    subtree_size = self.get_subtree_size(subtree_root)
    coord = self.get_treedata_coord(subtree_root) - 1
    attrfilename = self.attribute_filename(attribute)
    line_no = 0
    result = []
    with open(attrfilename, 'r') as f:
      for line in f:
        if line_no in range(coord, coord + subtree_size):
          result.append(json.loads(line.rstrip()))
        line_no += 1
    return result

  @staticmethod
  def prepare_attribute_values(generator, casting_fn=lambda x: x):
    result = defaultdict(list)
    for k, v in generator:
      result[int(k)].append(casting_fn(v))
    return result

  @staticmethod
  def prepare_attribute_values_from_tabular(filename, separator="\t",
        elem_field_num=0, attr_field_num=1, comment_char="#",
        casting_fn=lambda x: x):
    generator = attr_from_tabular_file.attribute_values(filename,
        elem_field_num, attr_field_num, separator, comment_char)
    return TreeAttributes.prepare_attribute_values(generator, casting_fn)

  def create_attribute(self, attribute, generator, casting_fn=lambda x: x,
                       force=False):
    """
    Creates a new attribute.

    The attribute values are given by the generator. The generator
    should yield pairs of the form (element_id, attribute_value).
    """
    self._check_filename_set()
    if self.has_attribute(attribute) and not force:
      raise error.AttributeCreationError(\
          f"Attribute '{attribute}' already exists")
    attribute_values = \
        TreeAttributes.prepare_attribute_values(generator, casting_fn)
    self.save_attribute_values(attribute, attribute_values)

  def create_attribute_from_tabular(self, attribute, filename,
      separator="\t", elem_field_num=0, attr_field_num=1, comment_char="#",
      casting_fn=lambda x: x, force = False):
    """
    Creates a new attribute.

    The attribute values are given in the tabular file.
    """
    self._check_filename_set()
    if self.has_attribute(attribute) and not force:
      raise error.AttributeCreationError(\
          f"Attribute '{attribute}' already exists")
    attribute_values = \
        TreeAttributes.prepare_attribute_values_from_tabular(filename,
          separator, elem_field_num, attr_field_num, comment_char, casting_fn)
    self.save_attribute_values(attribute, attribute_values)

  def save_attribute_values(self, attribute, attrvalues):
    self._check_filename_set()
    attrfilename = self.attribute_filename(attribute)
    logger.debug("Creating attribute file '{}'...".format(attrfilename))
    with open(attrfilename, "w") as outfile:
      for element_id in self.get_subtree_data(self.root_id):
        if element_id == self.UNDEF:
          attribute = None
        else:
          attribute = attrvalues.get(element_id, None)
        outfile.write(json.dumps(attribute) + "\n")

  def check_has_attributes(self, attributes):
    self._check_filename_set()
    for attribute in attributes:
      attrfilename = self.attribute_filename(attribute)
      if not attrfilename.exists():
        logger.error("Attribute '{}' not found".format(attribute))
        return False
    return True

  def query_attributes(self, subtree_root: int, attributes: List[str],
                       show_stats: bool = False) -> Dict[str, List[Any]]:
    """
    Returns attribute values for the given subtree, for multiple
    attributes, as a dictionary in the form {'attribute_name': [values]}.
    """
    result = {}
    for attrname in attributes:
      logger.debug("Loading attribute '{}' values".format(attrname))
      result[attrname] = self.subtree_attribute_data(subtree_root, attrname)
      if show_stats:
        filtered = [a for a in result[attrname] if a is not None]
        flattened = [e for sl in filtered for e in sl]
        logger.info("Number of nodes with attribute '{}': {}".\
            format(attrname, len(filtered)))
        logger.info("Number of values of attribute '{}': {}".\
            format(attrname, len(flattened)))
    return result

  def load_attribute_values(self, attribute):
    self._check_filename_set()
    self.__check_has_attribute(attribute)
    i = 0
    fname = self.attribute_filename(attribute)
    all_ids = self.get_subtree_data(self.root_id)
    existing = {}
    with open(fname, "r") as f:
      for line in f:
        data = json.loads(line.rstrip())
        if all_ids[i] != self.UNDEF:
          existing[all_ids[i]] = data
        i += 1
    return existing

  def dump_attribute_values(self, attribute):
    self._check_filename_set()
    self.__check_has_attribute(attribute)
    values = self.load_attribute_values(attribute)
    dump_fname = str(self.attribute_filename(attribute)) + ".json"
    with open(dump_fname, "w") as f:
      json.dump(values, f)

  def create_attribute_from_dump(self, attribute):
    self._check_filename_set()
    dump_fname = str(self.attribute_filename(attribute)) + ".json"
    with open(dump_fname, "r") as f:
      values = json.load(f)
    for k in list(values.keys()):
      values[int(k)] = values.pop(k)
    self.save_attribute_values(attribute, values)
    Path(dump_fname).unlink()

  def delete_attribute_values(self, attribute, node_ids, strict=False):
    """
    Delete the values of an attribute for a list of nodes.

    If strict is True, the node ids must be in the tree.
    Otherwise, nodes which do not exists are ignored.
    """
    values = self.load_attribute_values(attribute)
    for k in node_ids:
      k = int(k)
      if k in values:
        del values[k]
      elif strict:
        raise error.NodeNotFoundError(f"Node '{k}' not found in the tree")
    self.save_attribute_values(attribute, values)

  def append_attribute_values(self, attribute, newvalues, strict=False):
    """
    Append new values to an attribute.

    Given a dict of {node_id: [value,...]}, the values are appended to
    the existing values for the nodes. If strict is True, the node ids
    must be in the tree. Otherwise, nodes which do not exists are ignored.
    """
    values = self.load_attribute_values(attribute)
    for k in newvalues:
      if k in values:
        if values[k] is None:
          values[k] = newvalues[k]
        else:
          values[k].extend(newvalues[k])
      elif strict:
        raise error.NodeNotFoundError(f"Node '{k}' not found in the tree")
    self.save_attribute_values(attribute, values)

  def replace_attribute_values(self, attribute, newvalues, strict=False):
    """
    Replace the values of an attribute.

    Given a dict of {node_id: [value,...]}, the values replace the existing
    values for the nodes. If strict is True, the node ids must be in the tree.
    Otherwise, nodes which do not exists are ignored.
    The values for nodes not contained in newvalues are unchanged.
    """
    values = self.load_attribute_values(attribute)
    for k in newvalues:
      if k in values:
        values[k] = newvalues[k]
      elif strict:
        raise error.NodeNotFoundError(f"Node '{k}' not found in the tree")
    self.save_attribute_values(attribute, values)

