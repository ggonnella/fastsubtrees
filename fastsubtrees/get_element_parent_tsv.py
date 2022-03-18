from fastsubtrees import Tree

def getElementParentTSV(inputfile, nodefile):
    tree = Tree()
    with open(inputfile) as file:
        for f in file:
            fields = f.rstrip().split('\t')
            element = int(fields[0])
            parent = int(fields[1])
            tree.add_node(nodefile, parent, element)