class getElementParentIdFromTSV():
    def __init__(self, inputfile):
        self.inputfile = inputfile

    def getElementParentTSV(self):
        with open(self.inputfile) as file:
            for f in file:
                fields = f.rstrip().split('\t')
                element = int(fields[0])
                parent = int(fields[1])
                yield element, parent