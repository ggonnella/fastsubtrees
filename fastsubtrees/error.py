"""
Exceptions for the library
"""

class FastsubtreesError(Exception):
  """parent class for package-specific errors"""
  pass

class ConstructionError(FastsubtreesError):
  """error while constructing the tree"""
  pass
