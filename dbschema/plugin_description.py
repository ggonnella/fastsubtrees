#!/usr/bin/env python3
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, Float, String, DateTime,\
                       Boolean, Text, Enum
from sqlalchemy_repr import PrettyRepresentableBase
from sqlalchemy.dialects.mysql import DOUBLE

Base = declarative_base(cls=PrettyRepresentableBase)

utf8_cs_args = {'mysql_charset': 'utf8', 'mysql_collate': 'utf8_bin'}

class PluginDescription(Base):
  """
  Describes a plugin for assembly attributes computation.
  """
  __tablename__ = "pr_plugin_description"
  id = Column(String(256), primary_key=True)
  version = Column(String(64), primary_key=True)
  input = Column(String(512), nullable=False)
  output = Column(String(512), nullable=False)
  method = Column(Text(4096))
  implementation = Column((Text(4096)))
  parameters = Column((Text(4096)))
  req_software = Column(Text(4096))
  req_hardware = Column(Text(4096))
  advice = Column(Text(4096))
  __table_args__ = utf8_cs_args

