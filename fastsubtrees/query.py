"""
Subtree query operations for Tree() objects.
"""

import array
from typing import List, Dict, Any

class SubtreeQuery():

  def get_subtree_size(self, node: int) -> int:
    """
    Returns the number of nodes in the subtree rooted at the given node.
    """
    self._check_node_number(node)
    return self.subtree_sizes[node]

  def get_treedata_coord(self, node: int) -> int:
    """
    Returns the position of the given node in the treedata array.
    """
    self._check_node_number(node)
    return self.coords[node]

  def get_subtree_data(self, subtree_root: int) -> array.array:
    """
    Returns the treedata array for the subtree rooted at the given node.

    This includes nodes marked as deleted.
    """
    self._check_node_number(subtree_root)
    pos = self.get_treedata_coord(subtree_root)
    if pos > 0:
      subtree_size = self.get_subtree_size(subtree_root)
      return self.treedata[pos:pos + subtree_size]
    else:
      return array.array("Q")

  def subtree_ids(self, subtree_root: int) -> array.array:
    """
    Returns the IDs of the nodes in the subtree rooted at the given node.
    """
    self._check_node_number(subtree_root)
    result = array.array("Q")
    for node_id in self.get_subtree_data(subtree_root):
      if node_id != self.UNDEF:
        result.append(node_id)
    return result

  def subtree_info(self, subtree_root: int, attributes: List[str] = [],
                   include_subtree_sizes: bool = False,
                   include_parents: bool = False,
                   show_stats: bool = False,
                   node_id_key = "node_id",
                   subtree_size_key = "subtree_size",
                   parent_key = "parent") -> Dict[str, List[Any]]:
    result = {}
    node_ids = self.get_subtree_data(subtree_root)
    result[node_id_key] = node_ids
    if include_subtree_sizes:
      result[subtree_size_key] = []
      for node_id in node_ids:
        if node_id != self.UNDEF:
          result[subtree_size_key].append(self.get_subtree_size(node_id))
        else:
          result[subtree_size_key].append(None)
    if include_parents:
      result[parent_key] = []
      for node_id in node_ids:
        if node_id != self.UNDEF:
          result[parent_key].append(self.get_parent(node_id))
        else:
          result[parent_key].append(None)
    if attributes:
      attr_values = self.query_attributes(subtree_root, attributes, show_stats)
      for attrname in attributes:
        result[attrname] = attr_values[attrname]
    return result

