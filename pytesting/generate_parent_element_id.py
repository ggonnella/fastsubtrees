import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import yaml

parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from lib import db

class ElementParentIdGenerator():
    def __init__(self, configfile):
        with open(configfile) as file:
            data = yaml.safe_load(file)
        self.args = {"<dbname>": data['dbname'], "<dbuser>": data['dbuser'], "<dbpass>": data['dbpass'],
                     "<dbsocket>": data['dataroot'] + "mariadb/db.sock"}
        self.engine = create_engine(db.connstr_from(self.args), echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.conn = self.engine.connect()

    def get_element_parent_id(self):
        query = text('SELECT tax_id, parent_tax_id FROM nt_nodes')
        result = self.conn.execute(query).fetchall()
        for r in result:
            elem = r[0]
            parent = r[1]
            yield elem, parent