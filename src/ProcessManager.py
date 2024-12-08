import os
from operator import index
from types import new_class

import cv2
import numpy as math

import tkinter as tk

import numpy as np

from Classes.Quadrilateral import Quadrilateral

image = cv2.imread('templates/template3.png')



def createElementHTML(container, position,size):
    if container & type(container) is str:
        if type(position) is dict & type(size) is dict:
            open = "<" + container + "style="
            # the bloc of lines bellows is the coordinate position of the container
            top = "top =" + position["y"] + ";"
            right = "right =" + position["x"] + ";"
            bottom = "bottom =" + position["-y"] + ";"
            left = "left =" + position["-x"] + ";"
            # the bloc of lines bellows is the coordinate size of the container
            width = "width=" + size["x"] + ";"
            height = "height=" + size["y"] + ";"
            close = "</" + container +">"
            result = (
                    open +
                    top + right + bottom + left +
                    width + height +
                    close

            )
            return result

def getImage(template):
    root, ext = os.path.splitext(template)
    if ext == "png":
        print("first param meet requirement : success ! ")


def drawDot(blank_frame,position): return cv2.circle(blank_frame, position, 2, (0, 0, 255), -1)
def drawLine(frame, P1, P2): return cv2.line(frame, P1, P2, (0,0,255), 1)

def findCosines(P0, P1, P2):
    # find new vector because anchor point isn't 0,0 coordinate
    P1 = (P1[0] - P0[0], P1[1] - P0[1])
    P2 = (P2[0] - P0[0], P2[1] - P0[1])
    # find scalar product beetween the two points to know their "relation"
    scalarProduct = P1[0] * P2[0] + P1[1] * P2[1]
    # find the magnitude of each vector (hypothesis or norm)
    magnitude1 = math.sqrt(P1[0]**2 + P1[1]**2)
    magnitude2 = math.sqrt(P2[0]**2 + P2[1]**2)
    # finally calculate the cosinus
    cosinus = scalarProduct/(magnitude1 * magnitude2)
    # each result leads to a case
    if cosinus > 0:return False,"segments are adjacent", cosinus
    elif cosinus == 0: return True, "segments are perpendicular",cosinus
    elif cosinus < 0: return False, "segments are obtuse",cosinus

def findLowerUpperColor(colorName):
    colorsHSV = {
        "blue": [[100,150,0],[140,255,255]],
        "green": [[40,40,40],[80,255,255]],
        "red": [[0,70,70],[10,255,255]],
        "yellow": [[10,100,100],[30,255,255]],
        "orange": [[10,100,100],[20,255,255]],
        "white": [[0,0,200],[180,55,255]]
    }
    for name,HSV in colorsHSV.items():
        if name == colorName:
            return np.array(HSV[0], dtype=np.uint8), np.array(HSV[1],dtype=np.uint8)


def findColor(frame):
    #--- this is the set of colors
    colorsRGB = {
        "div" : [(0, 0, 255), "blue"],
        "nav" : [(0,255,0), "green"],
        "footer" : [(255,0,0),"red"],
        "header" : [(255,255,0),"yellow"],
        "section" : [(255, 165, 0),"orange"],
        "html" : [(255,255,255),"white"],
    }
    # --- define color range
    # -- red
    for container, info in colorsRGB.items():
        lowerColor, UpperColor = findLowerUpperColor(info[1])
        color = cv2.inRange(frame, lowerColor, UpperColor)
        if cv2.countNonZero(color) > 0:
            return info[1]


    #--- convert image to HSC to get efficient result
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# /!\ to draw a plan, each shape should be a quadrilateral
# If you drew a quadrilateral that has no space between the segments,
# it's possible that the function bellow doesn't the quadrilateral

def drawPlan():
    howManySides = 4 # because a quadrilateral is four-sided polygon

    image_borders = cv2.Canny(image, 150, 200)
    borders, _ = cv2.findContours(image_borders, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for border in borders:
        epsilon = 0.02 * cv2.arcLength(border, True)
        approx = cv2.approxPolyDP(border, epsilon, True)
        # get the coordinates of each points
        (x, y, w, h) = cv2.boundingRect(approx)
        #lambda to determine if there is 4 sides
        isFourSides = lambda : True if len(approx) == howManySides else False
        if isFourSides():
            print("The polygon has 4 sides, we can continue to make sure that this is a rectangle or a square...")
            # -------------- cos to find the angle
            # ------ step1 : coordinates of each sides
            A = (x,y) # --- side1
            B = (x + w, y) # --- side2
            C = (x + w, y + h) # --- side3
            D = (x , y + h) # --- side4
            #------ step 2 : find cos to determinate if two straight lines are perpendicular
            # --- what's the pattern ? every time, the letter increase so instead of call the function I will use that pattern to simplify my code using loop for
            sides = [A, B, C, D]
            blank_image = math.ones_like(image) * 255
            for side in sides:
                P0 = side
                P1 = lambda : sides[howManySides - 1] if sides.index(side) - 1 < 0 else sides[sides.index(side) - 1]
                P2 = lambda : sides[0] if sides.index(side) + 1 > len(sides) - 1 else sides[sides.index(side) + 1]
                print(P1(), P2())
                isQuadrilateral, message,result = findCosines(P0, P1(), P2())
                print(message + " this is the cosines : " + str(result))
                dots = drawDot(image, side)
                lines = drawLine(image,P0,P1())
                if not isQuadrilateral:
                    print("This is a polygon whit four sides but this is not a quadrilateral ")
            # At this point this is a quadrilateral because the requirements are met (four sides and each angles = 90°)
            # ---------------------------------------SHOW PLAN -----------------------#
            print(findColor(image))
            cv2.imshow("plan", image)
        elif not isFourSides():
            print("This is not a polygon with four sides ")
    return True

drawPlan()
cv2.waitKey(0)
cv2.destroyAllWindows()

