from fastsubtrees import error
class ElementParentIdGenerator():
    def __init__(self, inputfile):
        self.inputfile = inputfile

    def get_element_parent_id(self):
        with open(self.inputfile) as file:
            l = list()
            for f in file:
                fields = f.rstrip().split('\t')
                element = int(fields[0])
                parent = int(fields[1])
                if element in l:
                    raise error.NodeReplicationError('The node cannot have more than 1 parent')
                else:
                    l.append(element)
                    yield element, parent
