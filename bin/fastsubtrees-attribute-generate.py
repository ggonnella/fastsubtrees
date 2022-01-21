import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from lib import db

class GenerateAttributes():

    def __init__(self):
        self.args = {"<dbname>": "prostdb", "<dbuser>": "prostuser", "<dbpass>": "prostpass",
                "<dbsocket>": "/Users/amanmodi/Documents/prost-data/mariadb/db.sock"}
        self.engine = create_engine(db.connstr_from(self.args), echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.conn = self.engine.connect()
        self.attribute_list = list()

    def get_all_attributes(self):
        query = text('SELECT name FROM pr_attribute_definition')
        result = self.conn.execute(query).fetchall()
        for r in result:
            self.attribute_list.append(r[0]+'_v')
        return self.attribute_list

    def generate_attribute_file(self, attribute_list):
        with open(f"../data/attributes.json", "w") as outputfile:
            json.dump(attribute_list, outputfile)


g = GenerateAttributes()
attribute_list = g.get_all_attributes()
g.generate_attribute_file(attribute_list)
