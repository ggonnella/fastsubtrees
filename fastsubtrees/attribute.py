import json


class FinalAttributeGenerator():

    def get_attribute_value(self, attributefile, subtree_size, position):
        file = open(attributefile)
        data = json.load(file)
        print(len(data))
        attribute_value_list = list()
        for i in range(position, (position + subtree_size)):
            attribute_value_list.append(data[i])
        return attribute_value_list

    def get_attribute_list(self, tree, subtree_root, attributefile):
        treedata, position, subtree_size = tree.query_subtree(subtree_root)
        print(subtree_size)
        attribute_list = self.get_attribute_value(attributefile, subtree_size+1, position-1)
        return attribute_list
