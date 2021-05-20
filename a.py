from cv2 import cv2 
import math
import sympy
import time
from datetime import datetime

def getSlope(startPoint,endPoint):
    slope = (endPoint[1] - startPoint[1])/(endPoint[0]-startPoint[0])
    return slope

a = (1,1)
b = (5,5)

print(getSlope(a,b))