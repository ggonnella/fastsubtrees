#
# (c) Giorgio Gonnella, 2021
#
"""
Programmatically import a Python module and compile it on the
fly if it is an extension module written in Nim or Rust.
"""

import sh
import sys
import importlib
from pathlib import Path
import nimporter
import os
from contextlib import contextmanager

def py(filename, verbose=False):
  """
  Programmatically import Python module "filename"
  """
  modulename = Path(filename).stem
  spec = importlib.util.spec_from_file_location(modulename, filename)
  m = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(m)
  if verbose:
    sys.stderr.write(
        f"# python module {modulename} imported from file {filename}\n")
  m.__lang__ = "python"
  return m

def _retvals_to_module_attrs(m, prefix):
  for k in list(m.__dict__.keys()):
    if k.startswith(prefix):
      c = k[len(prefix):]
      setattr(m, c, getattr(m, k)())
      delattr(m, k)

def nim(filename, verbose=False, import_constants=True):
  """
  Import (and compile if necessary) a module written in Nim and
  based on Nimpy.

  Requirements:
  - Nim compiler
  - Nimporter

  import_constants option:
    if True, the return value of functions of the module whose name starts with
    "py_const_" (called without arguments) is stored as an attribute of the
    module (named without the aforementioned prefix), and the function is
    deleted from the module. This is a mechanism aimed at creating module-level
    constants.
  """
  modulename = Path(filename).stem
  parent = Path(filename).parent
  m = nimporter.Nimporter.import_nim_module(modulename, [parent])
  if import_constants:
    _retvals_to_module_attrs(m, "py_const_")
  if verbose:
    sys.stderr.write(
        f"# nim module {modulename} imported from file {filename}\n")
  m.__lang__ = "nim"
  return m

_toml_content = """
[package]
authors = ["*"]
name = "{modulename}"
version = "1.0.0"
edition = "2018"

[dependencies]
pyo3 = {{ version = "0.13.2", features = ["abi3-py36", "extension-module"] }}
{more_dependencies}

[lib]
name = "{modulename}"
crate-type = ["cdylib"]
path = "{modulename}.rs"
"""

def _create_cargo_toml(filename):
  """
  Create Cargo.toml for a pyo3/maturin module in the parent directory of
  <filename>.

  If the Rust code needs any crate, you can add a comment like:
  // [dependencies] foobar = "1.2.3"
  and this is added automatically to the [dependencies] section of Cargo.toml
  """
  workingdir = Path(filename).parent
  modulename = Path(filename).stem
  try:
    more_dependencies=sh.grep('\/\/ \[dependencies\] .*',
                              filename, P=True)
    more_dependencies=str(more_dependencies)[18:]
  except sh.ErrorReturnCode_1:
    more_dependencies=""
  with open(workingdir/"Cargo.toml", "w") as f:
    f.write(_toml_content.format(modulename = modulename,
                                more_dependencies=more_dependencies))

@contextmanager
def _cargo_for(filename):
  """
  Makes sure that a Cargo.toml exists for a module.
  If not, creates one using create_cargo_toml().
  If created, it is also deleted (and the Cargo.lock file too).
  """
  workingdir = Path(filename).parent
  cargo_temporary = False
  if not os.path.exists(workingdir/"Cargo.toml"):
    cargo_temporary = True
    _create_cargo_toml(filename)
  try:
    yield workingdir/"Cargo.toml"
  finally:
    if cargo_temporary:
      sh.rm(workingdir/"Cargo.toml", workingdir/"Cargo.lock")

def _transfer_attrs_to_module(m, membername):
  """
  Transfer attributes of a member of a module to the module
  and delete the member.

  Attribute starting with "_" are not transfered.

  If the member does not exist, nothing is done, silently.
  """
  if hasattr(m, membername):
    member = getattr(m, membername)
    for k in list(member.__dict__.keys()):
      if not k.startswith("_"):
        setattr(m, k, getattr(member, k))
    delattr(m, membername)

def rust(filename, verbose=False, import_constants=True):
  """
  Import a Rust module written using pyo3, compiling it with maturin.

  If no Cargo.toml is present (in the parent directory of <filename>),
  one is created by automatically (see _create_cargo_toml
  for details). In this case Cargo.toml and Cargo.lock are
  deleted after running the method.

  The "target" subdirectory (in the parent directory of <filename>) is not
  removed, so that unnecessary recompilations are avoided. You may want to add
  "target" to .gitignore.

  import_constants option:
    if a class "Constants" is defined in the module, all attributes of the class
    are moved to the module and the class is deleted (if import_constants is
    True); this mechanism is used in order to be able to define module-scoped
    constants.

  Requirements:
  - rust compiler and cargo
  - pyo3 (the maturin binary must be in path)
  """
  workingdir = Path(filename).parent
  modulename = Path(filename).stem
  with _cargo_for(filename) as cargo:
    sh.maturin("build", release=True, m=cargo)
  libfilename = workingdir/f"{modulename}.so"
  sh.ln(f"target/release/lib{modulename}.so", libfilename, s=True, f=True)
  spec = importlib.util.spec_from_file_location(modulename, libfilename)
  m = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(m)
  if import_constants:
    _transfer_attrs_to_module(m, "Constants")
  if verbose:
    sys.stderr.write(
        f"# python module {modulename} imported from file {filename}\n")
  m.__lang__ = "rust"
  return m

def importer(filename, verbose=False):
  """
  Import a module "filename", which is either a pure Python module
  or an extension module written in Nim or Rust. Set the __lang__ attribute
  of the module to "nim" or "python" or "rust".

  Assumptions:
  - Rust modules file suffix is ".rs"

  Requirements:
  - see requirements of rust() and nim() methods
  """
  if Path(filename).suffix == ".rs":
    m = rust(filename, verbose)
  else:
    try:
      m = py(filename, verbose)
    except:
      m = nim(filename, verbose)
  return m
