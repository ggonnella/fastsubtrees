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
  """error because node does not exist in the tree"""
  pass

class DuplicatedNodeError(FastsubtreesError):
  """duplicated node error, a node has more than 1 parent"""
  pass

class DeletedNodeError(FastsubtreesError):
  """cannot add a node which has already been deleted once"""
  pass

class FilenameNotSetError(FastsubtreesError):
  """the filename associated with tree is not set"""
  pass

class AttributeNotFoundError(FastsubtreesError):
  """trying to access an attribute which does not exist"""
  pass

class AttributeCreationError(FastsubtreesError):
  """attempted to create an attribute which already exists"""
  pass

