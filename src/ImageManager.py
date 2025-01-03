import os
import queue
import threading
import time
# This library is used to manage image
import cv2
# This library is used to extends mathematical functions
import numpy as math
import webcolors
from sympy.polys.heuristicgcd import heugcd

from src.classes.tag import Tag

image = cv2.imread('templates/Skeleton.png')
paper = math.ones_like(image) * 255

def drawDot(blank_frame,position): return cv2.circle(blank_frame, position, 2, (0, 0, 255), -1)
def drawLine(frame, P1, P2, thickness): return cv2.line(frame, P1, P2, (0,0,255), thickness)

def drawHatch(currentFrame,width, height):
    howManyTimes = 10
    # I didn't want the make the hatches too large or too small,  so the numerator is the width and the height
    divideX = width / howManyTimes
    divideY = height / howManyTimes

    currentPosX = width
    currentPosY = height
    # I want to connect every dot but if the quadrilateral isn't a square, the width or the height might have too much dot
    for dot in range(howManyTimes):
        drawDot(currentFrame, (currentPosX + divideX, currentPosY + divideY))

def findCosines(P0, P1, P2):
    # find new vector because anchor point isn't 0,0 coordinate
    P1 = (P1[0] - P0[0], P1[1] - P0[1])
    P2 = (P2[0] - P0[0], P2[1] - P0[1])
    # find scalar product beetween the two points to know their "relation"
    scalarProduct = P1[0] * P2[0] + P1[1] * P2[1]
    # find the magnitude of each vector (hypothesis or norm)
    magnitude1 = math.sqrt(P1[0]**2 + P1[1]**2)
    magnitude2 = math.sqrt(P2[0]**2 + P2[1]**2)
    # finally calculate the cosines
    cosines = scalarProduct/(magnitude1 * magnitude2)
    # each result leads to a case
    if cosines > 0:return False,"segments are adjacent", cosines
    elif cosines == 0: return True, "segments are perpendicular",cosines
    elif cosines < 0: return False, "segments are obtuse",cosines

def findColor(posX, posY):
    #--- this is the set of colors
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # --- define color range
    pixel = image_rgb[posY, posX]
    #f' means formatted string
    R,G,B = int(pixel[0]),int(pixel[1]),int(pixel[2])
    return R,G,B

#get center
def getCenter(A,B,C,D, quadrant):
    #---------------------------------------find the center of the square
    centerAB = (int((A[0] + B[0]) / 2), int((A[1] + B[1]) / 2))
    centerBC = (int((B[0] + C[0]) / 2), int((B[1] + C[1]) / 2))
    centerCD = (int((C[0] + D[0]) / 2), int((C[1] + D[1]) / 2))
    centerDA = (int((D[0] + A[0]) / 2), int((D[1] + A[1]) / 2))
    # coordinate center will be the intersection either AB vector and CD vector or BC vector DA vector
    center = (int((centerAB[0] + centerCD[0]) / 2), int((centerAB[1] + centerCD[1]) / 2))
    if quadrant == 1:
        return center, centerCD, centerDA # center, x, y
    elif quadrant == 2:
        return center, centerCD, centerBC # center, -x, y
    elif quadrant == 3:
        return center, centerAB, centerBC # center, -x, -y
    elif quadrant == 4:
        return center, centerAB, centerDA # center, x, -y

def infosContainer(containerInfos, center):
    textParam = [containerInfos,cv2.QT_FONT_NORMAL, 0.5, 2, 1]
    # recalculate anchor point of the text, because the location was upper, left, we need center, center
    print(cv2.getTextSize(textParam[0], textParam[1], textParam[2], textParam[3]))
    centerTextX, centerTextY = int(cv2.getTextSize(textParam[0], textParam[1], textParam[2], textParam[3])[0][0]/2) + int(center[0]), int((cv2.getTextSize(textParam[0], textParam[1], textParam[2], textParam[3])[0][1]/2)) + int(center[1])
    cv2.putText(paper,textParam[0], (centerTextX, centerTextY), textParam[1], textParam[2], (255,255,255),textParam[3])
# containers
def drawContener(x,y,w,h,containerType, isInlineStyling, result):
    width = None
    height = None
    center = None
    print("The polygon has 4 sides, we can continue to make sure that this is a rectangle or a square...")
    # ---------------------------------------coordinates of each sides----------------------------------------#
    A = (x,y) # --- side1
    B = (x + w, y) # --- side2
    C = (x + w, y + h) # --- side3
    D = (x , y + h) # --- side4
    sides = [A, B, C, D]
    # ---------------------------------find cos to find if each angle are at 90° -----------------------------#
    for side in sides:
        P0 = side
        P1 = lambda : sides[4 - 1] if sides.index(side) - 1 < 0 else sides[sides.index(side) - 1]
        P2 = lambda : sides[0] if sides.index(side) + 1 > len(sides) - 1 else sides[sides.index(side) + 1]

        isQuadrilateral, message,result = findCosines(P0, P1(), P2())
        if isQuadrilateral:
            print(message + " this is the cosines : " + str(result))
            # ------------------- proceed to draw the container on the paper
            drawDot(paper, side)
            drawLine(paper,P0,P1(), 2)
            # ------------------- proceed to put all the information center in the container
            width = A[0] - B[0]
            height = A[1] - D[1]
            center, centerX, centerY = getCenter(A,B,C,D,1)
        elif not isQuadrilateral:
            print("This is a polygon with four sides but this is not a quadrilateral ")
            return
    # put infos in container
    infos = f" container type : {containerType} \n width : {width} px \n height : {height} px \n coordinates position (absolute) : {center}"
    infosContainer(containerType,center)
    # create the tag
    tag = Tag(containerType, width, height)
    print(x,y,w,h,containerType, isInlineStyling, result)
    result.put(tag)
# let the user choose the type of container
def promptContainerType(functionDraw_container, result, x, y, w, h):
    valid_answer_container = ['div', 'section', 'nav', 'footer', 'header']
    valid_answer_isInlineStyling = ['yes', 'no', 'y','n', 'Yes', 'No','YES', 'NO', 'nO', 'yES', 'yEs','YEs','YeS', 'yeS']
    containerType = input("Insert your html container type here: ")
    while containerType not in valid_answer_container:
        print(containerType)
        containerType = input("This html container doesn't exist, please insert : ")

    isInlineStyling = input("Do you want to generate a css file ? (if your answer is no, the style will be in your html file): ")
    while isInlineStyling not in valid_answer_isInlineStyling:
        isInlineStyling = input("Your answer should be 'Yes' or 'No' : ")

    functionDraw_container(x, y, w, h, containerType, isInlineStyling, result)


# show the result of the original image
def showOriginalImage(oneFigure):
    cv2.drawContours(image, [oneFigure], -1,  (0, 255, 0), thickness=cv2.FILLED)
    cv2.imshow("image", image)

# draw the whole plan on a new frame
# /!\ to draw a plan, there is some rules :
# ---> quadrilaterals are containers
# ---> other shapes such as circle, triangles, polygons with 5+ sides are designs
#show infos
def drawPlan():
    geometry = {
        "circle" : 1,
        "segment" : 2,
        "triangle" : 3,
        "quadrilateral" : 4,
        "supTo4gon" : 5 # polygon with more than 4 sides
    }
    image_borders = cv2.Canny(image, 150, 200)
    borders, _ = cv2.findContours(image_borders, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    array_tags = []
    for border in borders:
        epsilon = 0.02 * cv2.arcLength(border, True)
        approx = cv2.approxPolyDP(border, epsilon, True)
        # get the coordinates of each points
        (x, y, w, h) = cv2.boundingRect(approx)
        #lambda to determine if there is 4 sides
        isOneSide = lambda : True if len(approx) == geometry["circle"] else False
        isTwoSide = lambda : True if len(approx) == geometry["segment"] else False
        isThreeSide = lambda : True if len(approx) == geometry["triangle"] else False
        isFourSides = lambda : True if len(approx) == geometry["quadrilateral"] else False
        isOtherSides = lambda : True if len(approx) == geometry["supTo4gon"] else False

        if isOneSide(): print("one side")
        elif isTwoSide(): print("two sides")
        elif isThreeSide(): print("okk")
        elif isFourSides():
            result = queue.Queue()
            task1 = threading.Thread(target=promptContainerType, args=(drawContener,result, x, y, w, h))
            task2 = threading.Thread(target=showOriginalImage, args=[border])

            task1.start()
            task2.start()

            task1.join()
            task2.join()
            result = result.get()
            print(result)

        elif isOtherSides(): print("other side")
    #html
    cv2.imshow("plan", paper)


drawPlan()
cv2.waitKey(0)
cv2.destroyAllWindows()

