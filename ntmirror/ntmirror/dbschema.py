#
# (c) 2020-2022 Giorgio Gonnella, University of Goettingen, Germany
#
"""
Defines the local database schema
"""

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String, \
                       Index, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_repr import PrettyRepresentableBase

# Nt = NCBI Taxonomy

Base = declarative_base(cls=PrettyRepresentableBase)

utf8_cs_args = {'mysql_charset': 'utf8', 'mysql_collate': 'utf8_bin'}

class NtName(Base):
  __tablename__ = 'nt_names'
  time_created = Column(DateTime, server_default=func.now())
  tax_id = Column(Integer, primary_key=True, autoincrement=False, index=True)
  name_txt = Column(String(256), primary_key=True)
  unique_name = Column(String(256), primary_key=True)
  name_class = Column(String(64), primary_key=True)
  __table_args__ = utf8_cs_args

  @classmethod
  def file_column_names(cls):
    return ["tax_id", "name_txt", "unique_name", "name_class"]

class NtGencode(Base):
  __tablename__ = 'nt_gencode'
  genetic_code_id = Column(Integer, primary_key=True, autoincrement=False)
  time_created = Column(DateTime, server_default=func.now())
  abbreviation = Column(String(64))
  name = Column(String(256))
  cde = Column(String(64))
  starts = Column(String(64))
  __table_args__ = utf8_cs_args

  @classmethod
  def file_column_names(cls):
    return ["genetic_code_id", "abbreviation", "name", "cde", "starts"]

class NtMerged(Base):
  __tablename__ = 'nt_merged'
  time_created = Column(DateTime, server_default=func.now())
  old_tax_id = Column(Integer, primary_key=True, autoincrement=False)
  new_tax_id = Column(Integer, index=True)
  __table_args__ = utf8_cs_args

  @classmethod
  def file_column_names(cls):
    return ["old_tax_id", "new_tax_id"]

class NtDivision(Base):
  __tablename__ = 'nt_division'
  division_id = Column(Integer, primary_key=True, autoincrement=False)
  time_created = Column(DateTime, server_default=func.now())
  division_cde = Column(String(3))
  division_name = Column(String(64))
  comments = Column(String(256))
  __table_args__ = utf8_cs_args

  @classmethod
  def file_column_names(cls):
    return ["division_id", "division_cde", "division_name", "comments"]

class NtDelnode(Base):
  __tablename__ = 'nt_delnodes'
  tax_id = Column(Integer, primary_key=True, autoincrement=False)
  __table_args__ = utf8_cs_args

  @classmethod
  def file_column_names(cls):
    return ["tax_id"]

class NtCitation(Base):
  __tablename__ = 'nt_citations'
  cit_id = Column(Integer, primary_key=True, autoincrement=False)
  cit_key = Column(String(256))
  pubmed_id = Column(Integer)
  medline_id = Column(Integer)
  url = Column(String(1024))
  text = Column(Text)
  taxid_list = Column(Text(1000000))
  __table_args__ = utf8_cs_args

  @classmethod
  def file_column_names(cls):
    return ["cit_id", "cit_key", "pubmed_id", "medline_id", "url", "text",
            "taxid_list"]

class NtNode(Base):
  __tablename__ = 'nt_nodes'
  tax_id = Column(Integer, primary_key=True, autoincrement=False)
  parent_tax_id = Column(Integer, index=True)
  rank = Column(String(64), index=True)
  embl_code = Column(String(64))
  division_id = Column(Integer)
  inherited_div_flag = Column(Boolean)
  genetic_code_id = Column(Integer)
  inherited_GC_flag = Column(Boolean)
  mitochondrial_genetic_code_id = Column(Integer)
  inherited_MGC_flag = Column(Boolean)
  GenBank_hidden_flag = Column(Boolean)
  hidden_subtree_root_flat = Column(Boolean)
  comments = Column(String(1024))
  __table_args__ = utf8_cs_args

  @classmethod
  def file_column_names(cls):
    return ["tax_id", "parent_tax_id", "rank", "embl_code", "division_id",
            "inherited_div_flag", "genetic_code_id", "inherited_GC_flag",
            "mitochondrial_genetic_code_id", "inherited_MGC_flag",
            "GenBank_hidden_flag", "hidden_subtree_root_flat", "comments"]

tablename2class = {
  'nt_names': NtName,
  'nt_gencode': NtGencode,
  'nt_merged': NtMerged,
  'nt_division': NtDivision,
  'nt_delnodes': NtDelnode,
  'nt_citations': NtCitation,
  'nt_nodes': NtNode,
}

FILE2CLASS = {
  'names': NtName,
  'gencode': NtGencode,
  'merged': NtMerged,
  'division': NtDivision,
  'delnodes': NtDelnode,
  'citations': NtCitation,
  'nodes': NtNode,
}

DB_MODEL_CLASSES = tablename2class.values()

def create(connection):
  for klass in DB_MODEL_CLASSES:
    klass.metadata.create_all(connection)

def drop(connection):
  for klass in DB_MODEL_CLASSES:
    klass.metadata.drop_all(connection)
