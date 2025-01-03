import json

class Tag:
    index = 0
    isInlineStyle = False
    # ---------------------------------- html
    line = None # class : formatted string
    parent  = None # class : Tag
    # ----------------------------------  style (css)
    # identified by skeleton
    width = None
    height = None
    grid_row = 1
    grid_line = 1

    # identified by skin
    background_color = None
    border_color = None
    border = None

    # ---------------------------------  script (js)
    def __init__(self, tag, width, height):
        self.index += 1
        self.tag = self.buildTag(tag)

        self.width = width
        self.height = height

    # generate tag
    def setParentObligations(self, parentPosX, parentPosY):
        # rule 1 : if the container became a parent of multiple children then it must generate a cells
        with open('data/data.json', 'e') as file:
            output = json.load(file)
        for dict in output:
            print(dict)

    def convertPx(self, unitOfMeasurement, imageSize):
        if unitOfMeasurement == 'v' or unitOfMeasurement == 'viewport':
            return self.width/imageSize[0], self.height/imageSize[1]

    def buildTag(self, containerType):
        tag = f"<{containerType}></{containerType}>"
        if self.getIsInlineStyle():
            tag = f"<{containerType} style= width: {self.getWidth()} height: {self.getHeight()} grid-row: {self.getGridRow()} grid-line {self.getLine()}></{containerType}>"
            return tag, False
        return tag, True

    # classic methods
    def saveTags(self, tags):
        with open('data/data.json', 'w', encoding="utf-8") as file:
            # indent has two choice : 4 or 8. 8 = datas will be in one line
            json.dump({tags},file,indent=4,ensure_ascii=False)

    # getters and setters
    def setIsInlineStyle(self, isInlineStyle): self.isInlineStyle = isInlineStyle

    def getIsInlineStyle(self): return self.isInlineStyle
    def getTag(self): return self.tag
    def getIndex(self): return self.index
    def getLine(self): return self.line
    def getParent(self): return self.parent
    def getWidth(self): return self.width
    def getHeight(self): return self.height
    def getGridRow(self): return self.grid_row
    def getGridLine(self): return self.grid_line
    def getBackgroundColor(self): return self.background_color
    def getBorderColor(self): return self.border_color
    def getBorder(self): return self.border

