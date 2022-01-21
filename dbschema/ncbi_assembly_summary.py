#!/usr/bin/env python3

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String, \
                       Index, DateTime, Date, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_repr import PrettyRepresentableBase
import enum

# Nas = NCBI Assembly Summary

Base = declarative_base(cls=PrettyRepresentableBase)

utf8_cs_args = {'mysql_charset': 'utf8', 'mysql_collate': 'utf8_bin'}

class NcbiAssemblySummary(Base):
  __tablename__ = 'ncbi_assembly_summary'
  accession = Column(String(15), primary_key=True)
  time_updated = Column(DateTime,
      server_default=func.now(), onupdate=func.now())
  seqdb = Column(Enum("refseq", "genbank"))
  domain = Column(Enum("bacteria", "archaea"))
  bioproject = Column(String(11))
  biosample = Column(String(14))
  wgs_master = Column(String(32))
  refseq_category = Column(Enum("representative genome",
    "reference genome"))
  taxid = Column(Integer)
  species_taxid = Column(Integer)
  organism_name = Column(String(256))
  infraspecific_name = Column(String(256))
  isolate = Column(String(256))
  version_status = Column(Enum("latest"))
  assembly_level = Column(Enum("Contig", "Scaffold", "Complete Genome",
    "Chromosome"))
  release_type = Column(Enum("Minor", "Major"))
  genome_rep = Column(Enum("Full", "Partial"))
  seq_rel_date = Column(Date)
  asm_name = Column(String(256))
  submitter = Column(Text(2048))
  gbrs_paired_asm = Column(String(15))
  paired_asm_comp = Column(Enum("identical", "different"))
  ftp_path = Column(String(256))
  excluded_from_refseq = Column(String(256))
  relation_to_type_material = Column(Enum(
    "assembly from type material",
    "assembly from synonym type material",
    "assembly from pathotype material",
    "assembly designated as reftype",
    "assembly designated as neotype"))
  __table_args__ = utf8_cs_args

