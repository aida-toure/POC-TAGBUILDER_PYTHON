class Quadrilateral:
    #attributes
    typeHTML = None
    #constructor
    def __init__(self, side1, side2, side3, side4, _):
        self.typeHTML = self
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        self.side4 = side4
    # getters and setters
    def getSide1(self):return self.side1
    def getSide2(self):return self.side2
    def getSide3(self):return self.side3
    def getSide4(self):return self.side4

    def getTypeHTML(self):return self.typeHTML



