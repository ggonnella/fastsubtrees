class ElementParentIdGenerator():
    def __init__(self, inputfile):
        self.inputfile = inputfile

    def get_element_parent_id(self):
        with open(self.inputfile) as file:
            for line in file:
                if line[0] == "#":
                  continue
                fields = line.rstrip().split('\t')
                element = int(fields[0])
                parent = int(fields[1])
                yield element, parent
