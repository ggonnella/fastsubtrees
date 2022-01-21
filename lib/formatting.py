def shorten(s: str, limit: int, placeholder: str = "...") -> str:
  """
  Shorten a string to a string with maximum length limit.

  If the string is longer than limit, the string is shortened
  to limit - len(placeholder) character and the placeholder is added.
  """
  assert(limit >= len(placeholder))
  return s if len(s) <= limit else s[:limit-len(placeholder)] + placeholder
