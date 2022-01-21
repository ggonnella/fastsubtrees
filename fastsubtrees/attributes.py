import json
from dbschema.attribute import AttributeValueTables
from fastsubtrees import Tree, _scripts_support
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from lib import db


class Attributes():

    @staticmethod
    def get_table_name(session, engine, attribute):
        avt = AttributeValueTables(engine)
        attributes = dict()
        table_name = ''
        for k in avt.table_suffixes:
            q = session.query(avt.get_class(k)).statement.columns.keys()
            attributes[str(avt.get_class(k))] = q
        for key, value in attributes.items():
            for val in value:
                if attribute == val:
                    table_name = key
        return table_name

    @staticmethod
    def create_json_file(attribute, attribute_value):
        with open(f"../data/{attribute}.json", "w") as outfile:
            json.dump(attribute_value, outfile)


    def get_attribute_list(self, inputfile, subtreeroot, passedattribute):
        arguements = {"<dbname>": "prostdb", "<dbuser>": "prostuser", "<dbpass>": "prostpass",
                      "<dbsocket>": "/Users/amanmodi/Documents/prost-data/mariadb/db.sock"}
        engine = create_engine(db.connstr_from(arguements), echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        conn = engine.connect()
        tree = Tree.from_file(inputfile)
        subtree_root = int(subtreeroot)
        attribute = passedattribute
        subtree_ids = tree.subtree_ids(subtree_root)[0]
        accessions = list()
        attribute_value = list()
        table_name = self.get_table_name(session, engine, attribute)
        for id in subtree_ids:
            initial_accessions = list()
            query = text(f'SELECT accession FROM ncbi_assembly_summary WHERE taxid={id}')
            result = conn.execute(query).fetchall()
            for r in result:
                initial_accessions.append(r[0])
            accessions.append(initial_accessions)
        for l in accessions:
            i_list = list()
            if len(l) > 1:
                for accession in l:
                    query2 = text(f'SELECT {attribute} FROM {table_name} WHERE accession="{accession}"')
                    result2 = conn.execute(query2).fetchall()
                    if len(result2) > 0:
                        i_list.append(result2[0][0])
                if len(i_list) > 0:
                    attribute_value.append(i_list)
                else:
                    attribute_value.append(None)
            else:
                attribute_value.append(None)
        return attribute_value

    def get_attribute_value(self, attributefile, subtree_size, position):
        file = open(attributefile)
        data = json.load(file)
        attribute_value_list = list()
        for i in range(position,(position+subtree_size)):
            attribute_value_list.append(data[i])
        return attribute_value_list




