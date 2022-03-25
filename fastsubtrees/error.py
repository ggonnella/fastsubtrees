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

class NodeReplicationError(FastsubtreesError):
  """repeating node error, a node has more than 1 parent"""
  pass