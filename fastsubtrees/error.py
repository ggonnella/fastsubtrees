"""
Exceptions for the library
"""

class FastsubtreesError(Exception):
  """parent class for package-specific errors"""
  pass

class ConstructionError(FastsubtreesError):
  """error while constructing the tree"""
  pass

class NodeNotFoundError(FastsubtreesError):
  """error while querying the tree"""
  pass

class DuplicatedNodeError(FastsubtreesError):
  """duplicated node error, a node has more than 1 parent"""
  pass

class RootNotFoundError(FastsubtreesError):
  """no root node exist for the given tree"""
  pass

class MultipleRootNodeError(FastsubtreesError):
  """multiple root nodes cannot exist for a tree"""
  pass

class ParentNotFoundError(FastsubtreesError):
  """parent does not exist for a given child node"""
  pass

class DeletedNodeError(FastsubtreesError):
  """cannot add a node which has already been deleted once"""
  pass
