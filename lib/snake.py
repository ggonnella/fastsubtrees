"""
Helper functions for scripts
"""

def setargs(args, src, *names):
  """
  For each name in <names>, set args[name] to
  src.get(key), where key is a transformation of the name
  as decribed below.

  This is to facilitate scripts to be called directly
  with option parsing by docopt or via snakemake "script".

  The <names> must be strings such those returned by docopt,
  i.e. starting with "--" or enclosed in "<>".
  The key is derived from the name by removing these formatting chars
  and replacing internal "-" with underscores.
  If a key is not available, args[name] is set to None.

  Alternatively instead of a string, a 2-tuple of strings
  can be passed (name, key).

  E.g. setargs(args, snakemake.input, "<file>")
       => args["<file>"] = snakemake.input.get("file")
       setargs(args, snakemake.params, "--long-opt")
       => args["--long-opt"] = snakemake.params.get("long_opt")
  """
  for name in names:
    if isinstance(name, tuple):
      key = name[1]
      name = name[0]
    else:
      if name.startswith("--"):
        key = name[2:]
      else:
        assert(name[0]=="<")
        assert(name[-1]==">")
        key = name[1:-1]
      key = key.replace("-","_")
    args[name] = src.get(key)

def args(snakemake, *dicts, **kwargs):
  """
  Create a args dict similar to the result of docopt,
  using the snakemake variable.

  First usage: one provides named arguments, which are lists of strings,
  where the name of the argument is the property of "snakemake" where
  to take the value from. The values are arguments keys, from which the keys
  of the snakemake property are computed, by removing the "--" or "<>".

  e.g.
    args(snakemake, input=["<a>, "--b"], params=["--c", "<d>"],
                    output=["--e", "<f>"], config=["<g>, "--h"],
                    log=["--i", "<j>"])

  Second usage: instead or in addition to the previous, one provides
  dicts which contains lists of strings with key strings which are the
  properties of "snakemake". This allows to pass pre-defined lists of
  argument keys.

  e.g.
    args(snakemake, {"input": ["<a>"], "params": ["--b"]},
                    {"input": ["<c>, "--d"], "output": ["<e>"]},
                    input=["<f>, "--g"], params=["--h"])
  or:
    args(snakemake, my_module.predefined_args_list,
                    other_module.other_list,
                    input=["<f>, "--g"], params=["--h"])

  It is possible to override a key passed as one of the dicts, in one of the
  following dicts, or in the kwargs. However, one should avoid to use the same
  key multiple times in the same dict or in the keyed args, as in this case
  the behaviour is random!
  """
  args = {}
  for d in dicts:
    for k, v in d.items():
      setargs(args, getattr(snakemake, k), *v)
  for k, v in kwargs.items():
    setargs(args, getattr(snakemake, k), *v)
  return args
