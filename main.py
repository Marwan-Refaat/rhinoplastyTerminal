from cv2 import cv2 
import math
import sympy
import os
from datetime import datetime

path = "testImage.jpg"
img = cv2.imread(path)

currentMode = 0
currentImgCount = 0

unitDistance = 0.0

def getSlope(startPoint,endPoint):
    #Slope = Rise/Run
    slope = (endPoint[1] - startPoint[1])/(endPoint[0]-startPoint[0])

    #y=mx+b => b = y-mx
    yInt = endPoint[1] - slope*endPoint[0]

    return slope,yInt



def undoImg():
    global currentImgCount
    global img
    #Undo Image
    if currentImgCount == 0:
        img = cv2.imread(path)
    else:
        imagePath = "cache/image"+str(currentImgCount-1)+".jpg"
        img = cv2.imread(imagePath)
        os.remove(imagePath)
        updateCounter(-1)

def cacheImg():
    global img

    #Defining path for cached image and saving it in cache folder
    imagePath = "cache/image"+str(currentImgCount)+".jpg"
    cv2.imwrite(imagePath,img)
    updateCounter(1)

def updateCounter(num):
    global currentImgCount

    if num == 1:
        currentImgCount+=1
    elif num == -1:
        currentImgCount-=1


######## Legan's Mode functions ##########
def leganMode():
    #Global img variable, used to refresh image
    global img
    
    pointsList = []

    #Saving Image to cache
    cacheImg()
    
    #Setting mouse callback to the legan method function
    cv2.setMouseCallback('Image',leganFunction,[pointsList])

    while True:
        cv2.imshow('Image',img)


        if (cv2.waitKey(100) & 0xFF == ord('e') or len(pointsList) >= 5): #Exit Current Mode
            print("Do you want to save these changes?(Y/N)")
            key = cv2.waitKey(0)
            #If saving changes, do nothing to image
            if key & 0xFF == ord('y'):
                cacheImg()
                break
            #If not saving,reset image to previous state and delete cached image
            elif key & 0xFF == ord('n'):
                undoImg()
                break
            else:
                print("Do you want to save these changes?(Y/N)")
                key = cv2.waitKey(0)


def leganFunction(event,x,y,flags,params):
    pointsList = params[0] 
    if (event == cv2.EVENT_LBUTTONDOWN) and (len(pointsList) < 4) : #Left Click and <4 points exist
        
        #Draw Point
        cv2.circle(img,(x,y),2,(0,0,255),cv2.FILLED)
        
        #Add to points list
        pointsList.append((x,y))
        print("Point drawn at:"+str(x) +"," + str(y))
        print(pointsList)

        #Factor used in extending line (Change to extend lines more or less)
        extensionFactor = 50
        if len(pointsList) == 2:#If 2 points drawn
            #Get slope of line
            slope,yInt = getSlope(pointsList[0],pointsList[1])
            
            if pointsList[0][0] > pointsList[1][0]:
                extensionFactor = -extensionFactor

            #Extend Points
            startX = int(pointsList[0][0]-extensionFactor)
            startY = int(startX*slope + yInt)
            newStartPoint = (startX,startY)

            endX= int(pointsList[1][0]+extensionFactor)
            endY = int(endX*slope + yInt)
            newEndPoint = (endX,endY)

            #Draw Line between extended points
            cv2.line(img,newStartPoint,newEndPoint,(255,255,255),2)
            print("Line Drawn at:"+str(newStartPoint)+","+str(newEndPoint))
        elif len(pointsList) == 4:#If 4 points drawn
            #Get slope of line
            slope,yInt = getSlope(pointsList[2],pointsList[3])
            
            if pointsList[2][0] > pointsList[3][0]:
                extensionFactor = -extensionFactor

            #Extend Points
            startX = int(pointsList[2][0]-extensionFactor)
            startY = int(startX*slope + yInt)
            newStartPoint = (startX,startY)

            endX= int(pointsList[3][0]+extensionFactor)
            endY = int(endX*slope + yInt)
            newEndPoint = (endX,endY)

            #Draw Line between last two points
            cv2.line(img,newStartPoint,newEndPoint,(255,255,255),2)
            print("Line Drawn at:"+str(newStartPoint)+","+str(newEndPoint))

            #Get angle between two lines
            l1 = sympy.Line(pointsList[0],pointsList[1])
            l2 = sympy.Line(pointsList[2],pointsList[3])
            
            #Print angle in degrees
            print("Legan Angle is: ",math.degrees(l1.smallest_angle_between(l2)))



######## Silver's Mode functions ##########
def silverMode():
    print("Entered Silver's Method Mode")
    print("Please draw point of elevation for Frankfort horizontal line")
    #Global img variable, used to refresh image
    global img
    
    pointsList = []

    #Saving Image to cache
    cacheImg()
    
    #Setting mouse callback to the legan method function
    cv2.setMouseCallback('Image',silverFunction,[pointsList])

    while True:
        cv2.imshow('Image',img)

        #If distance calibration has not been completed before
        if unitDistance == 0.0:
            print("Please enter distance calibration mode first before entering Silver's Method mode")
            undoImg()
            break

        if (cv2.waitKey(100) & 0xFF == ord('e') or len(pointsList) >= 5): #Exit Current Mode
            print("Do you want to save these changes?(Y/N)")
            key = cv2.waitKey(0)
            #If saving changes, do nothing to image
            if key & 0xFF == ord('y'):
                cacheImg()
                break
            #If not saving,reset image to previous state and delete cached image
            elif key & 0xFF == ord('n'):
                undoImg()
                break
            else:
                print("Do you want to save these changes?(Y/N)")
                key = cv2.waitKey(0)



def silverFunction(event,x,y,flags,params):
    #Defining unit distance as global to avoid errors
    global unitDistance

    pointsList = params[0] 
    if (event == cv2.EVENT_LBUTTONDOWN) and (len(pointsList) < 3) : #Left Click and <3 points exist
        
        #Draw Point
        cv2.circle(img,(x,y),2,(0,0,255),cv2.FILLED)
        
        #Add to points list
        pointsList.append((x,y))
        print("Point drawn at:"+str(x) +"," + str(y))
        print(pointsList)

        #Factor used in extending line (Change to extend lines more or less)
        extensionFactor = 450


            

        if len(pointsList) == 1: #Placing Point of elevation
            
            #Extend Line points
            startPointX = pointsList[0][0] - extensionFactor
            startPointY = pointsList[0][1]
            startPoint = (startPointX,startPointY)

            endPointX = pointsList[0][0] + extensionFactor
            endPointY = pointsList[0][1]
            endPoint = (endPointX,endPointY)

            #Draw Line
            cv2.line(img,startPoint,endPoint,(0,0,255),2)

            print("Please draw point to draw vertical line")
        
        elif len(pointsList) == 2: #Draw vertical line
            #Extend Line points
            startPointX = pointsList[1][0] 
            startPointY = pointsList[1][1] - extensionFactor
            startPoint = (startPointX,startPointY)

            endPointX = pointsList[1][0] 
            endPointY = pointsList[1][1] + extensionFactor
            endPoint = (endPointX,endPointY)

            #Draw Line
            cv2.line(img,startPoint,endPoint,(0,0,255),2)
            print("Please draw measuring point")

        elif len(pointsList) == 3: #Placing measuring point
            
            #Extend Line points
            startPointX = pointsList[1][0] 
            startPointY = pointsList[1][1] - extensionFactor
            startPoint = (startPointX,startPointY)

            endPointX = pointsList[1][0] 
            endPointY = pointsList[1][1] + extensionFactor
            endPoint = (endPointX,endPointY)


            s1 = sympy.Segment(startPoint,endPoint)
            shortestDistance = s1.distance(pointsList[2])
            measuredDistance = shortestDistance*unitDistance
            #print("Shortest distance is: ",shortestDistance)
            print("Measured distance is: ",measuredDistance)

            #Intersection point is x-coordinate of vertical line and y-coordinate of measuring point
            intersectionPoint = (startPointX,pointsList[2][1])

            #Draw line between measuring point and Frankfort line
            cv2.line(img,pointsList[2],intersectionPoint,(0,0,255),2)



######## Goode's Mode functions ##########
def goodeMode():
    print("Entered Goode's Method Mode")
    print("Please place vertex A on Image")
    #Global img variable, used to refresh image
    global img
    
    pointsList = []

    #Saving Image to cache
    cacheImg()
    
    #Setting mouse callback to the legan method function
    cv2.setMouseCallback('Image',goodeFunction,[pointsList])

    while True:
        cv2.imshow('Image',img)

        #If distance calibration has not been completed before
        if unitDistance == 0.0:
            print("Please enter distance calibration mode first before entering Goode's Method mode")
            undoImg()
            break

        if (cv2.waitKey(100) & 0xFF == ord('e') or len(pointsList) >= 5): #Exit Current Mode
            print("Do you want to save these changes?(Y/N)")
            key = cv2.waitKey(0)
            #If saving changes, do nothing to image
            if key & 0xFF == ord('y'):
                cacheImg()
                break
            #If not saving,reset image to previous state and delete cached image
            elif key & 0xFF == ord('n'):
                undoImg()
                break
            else:
                print("Do you want to save these changes?(Y/N)")
                key = cv2.waitKey(0)



def goodeFunction(event,x,y,flags,params):
    #Defining unit distance as global to avoid errors
    global unitDistance

    pointsList = params[0] 
    if (event == cv2.EVENT_LBUTTONDOWN) and (len(pointsList) < 3) : #Left Click and <5 points exist
        
        #Draw Point
        cv2.circle(img,(x,y),2,(0,0,255),cv2.FILLED)
        
        #Add to points list
        pointsList.append((x,y))
        print("Point drawn at:"+str(x) +"," + str(y))
        print(pointsList)

         
        if len(pointsList) == 1: #Placing Point A of triangle

            print("Vertex A drawn, please place vertex B on image")
        
        elif len(pointsList) == 2: #Placing measuring point
            #Draw Line
            cv2.line(img,pointsList[0],pointsList[1],(0,0,255),2)

            print("Vertex B placed, please draw vertex C")


        elif len(pointsList) == 3:
            
            #Draw Line
            cv2.line(img,pointsList[1],pointsList[2],(0,0,255),2)
            cv2.line(img,pointsList[0],pointsList[2],(0,0,255),2)
            
            edgeAB = sympy.Segment(pointsList[0],pointsList[1])
            edgeBC = sympy.Segment(pointsList[1],pointsList[2])
            edgeAC = sympy.Segment(pointsList[0],pointsList[2])

            lengthAB = edgeAB.length * unitDistance
            lengthBC = edgeBC.length * unitDistance
            lengthAC = edgeAC.length * unitDistance

            #print("Shortest distance is: ",shortestDistance)
            print("Length of edge AB is: ",str(float(lengthAB)))
            print("Length of edge BC is: ",str(float(lengthBC)))
            print("Length of edge AC is: ",str(float(lengthAC)))




######## Measuring Mode functions ##########
def measuringMode():

    global measuringUndoCount
    global unitDistance
    global img
    
    pointsList = []

    #Saving version of image to cache
    cacheImg()

    

    while True:
        cv2.imshow('Image',img)

        if unitDistance == 0.0:
            print("Please enter distance calibration mode first before measuring objects")
            undoImg()
            cacheImg()
            break

        #Setting mouse callback to the measuring function
        cv2.setMouseCallback('Image',measuringFunction,[pointsList])
        key = cv2.waitKey(100) & 0xFF 

        if (key == ord('e')): #Exit Current Mode
            print("Do you want to save these changes?(Y/N)")
            key = cv2.waitKey(0)
            #If saving changes, save current changes to image
            if key & 0xFF == ord('y'):
                cacheImg()
                break
            #If not saving,reset image to previous state and delete cached image
            elif key & 0xFF == ord('n'):
                
                undoImg()
                cacheImg()
                break
            else:
                print("Do you want to save these changes?(Y/N)")
                key = cv2.waitKey(0)
            break
        
        elif (key == ord('r')): #Restart Calibration Mode
            print("Calibration Reset")
            #Reset unit distance and remove points
            unitDistance = 0.0
            pointsList = []

            #Undo Image
            undoImg()

            

measuringUndoCount = 0           
def measuringFunction(event,x,y,flags,params):
    global measuringUndoCount
    global unitDistance
    pointsList = params[0] 
    if (event == cv2.EVENT_LBUTTONDOWN): #Left Click and <4 points exist
        
        if len(pointsList) >= 4: #If 3rd line is placed, clear all lines and remove last line from points list
            print("REMOVING LAST TWO POINTS NOW")
            print(pointsList)
            pointsList.pop()
            pointsList.pop()
            
            print(pointsList)
            
            #Undo Image
            if measuringUndoCount == 0:
                undoImg()
                measuringUndoCount+=1

            

        #Draw Point
        cv2.circle(img,(x,y),2,(0,0,255),cv2.FILLED)
        
        #Add to points list
        pointsList.append((x,y))
        print("Point drawn at:"+str(x) +"," + str(y))
        print(pointsList)

        
        if len(pointsList) == 2:#If 2 points drawn
            #Draw Line between two points
            cv2.line(img,pointsList[0],pointsList[1],(0,0,255),2)
            pixelDistance = math.sqrt(((pointsList[0][0] - pointsList[1][0])**2 + (pointsList[0][1] - pointsList[1][1])**2) )

            print("Unit Distance: ",unitDistance)
            print("Pixel Distance: ",pixelDistance)
            measuredDistance = unitDistance*pixelDistance
            print("Measured Distance is: ",measuredDistance)
        
        elif len(pointsList) == 4:
            #Draw Line between two points
            cv2.line(img,pointsList[2],pointsList[3],(0,0,255),2)
            pixelDistance = math.sqrt(((pointsList[2][0] - pointsList[3][0])**2 + (pointsList[2][1] - pointsList[3][1])**2) )

            print("Unit Distance: ",unitDistance)
            print("Pixel Distance: ",pixelDistance)
            measuredDistance = unitDistance*pixelDistance
            print("Measured Distance is: ",measuredDistance)


            
######## Calibration Mode functions ##########

def calibrationMode():

    global unitDistance
    global img
    
    pointsList = []

    #Saving version of image to cache
    cacheImg()

    #Setting image to initial state to easily calibrate distance
    img = cv2.imread(path)
    
    print("Please draw the calibration line")
    while True:
        cv2.imshow('Image',img)


        #Setting mouse callback to the measuring function
        cv2.setMouseCallback('Image',calibrationFunction,[pointsList])
        key = cv2.waitKey(100) & 0xFF 

        if (key == ord('e')): #Exit Current Mode
            print("Exited Calibration Mode")
            
            #Undo Image
            undoImg()
            break
            

          
def calibrationFunction(event,x,y,flags,params):
    
    global unitDistance

    pointsList = params[0] 
    if (event == cv2.EVENT_LBUTTONDOWN and len(pointsList)<2): #Left Click and <2points exist
              

        #Draw Point
        cv2.circle(img,(x,y),2,(0,0,255),cv2.FILLED)
        
        #Add to points list
        pointsList.append((x,y))
        print("Point drawn at:"+str(x) +"," + str(y))
        print(pointsList)

        
        if len(pointsList) == 2:#If 2 points drawn
            #Draw Line between two points
            cv2.line(img,pointsList[0],pointsList[1],(0,0,255),2)
            userDistance = input("Calibration Line drawn, please enter distance: ") 
            
            pixelDistance = math.sqrt(((pointsList[0][0] - pointsList[1][0])**2 + (pointsList[0][1] - pointsList[1][1])**2) )
            unitDistance = float(userDistance)/pixelDistance
        
            print("Calibration Complete, please press E to exit calibration mode")



#Main Loop
while True:
    cv2.imshow('Image',img)

    #Clearing mouse callback to unbind functions from left click after leaving modes
    cv2.setMouseCallback('Image', lambda *args : None)

    print("Begin Input Mode")
    print("------LEGEND------")
    print("C - Clear Image Completely")
    print("Z - Undo Last Image Modification")
    print("L - Legan's Method Mode")
    print("S - Silver's Method Mode")
    print("G - Goode's Method Mode")
    print("M - Measuring Mode")
    print("D - Distance Calibration Mode")
    print("E - Exit Program")
    key = cv2.waitKey(0)
    #cmd = input("Enter Command: ")
    if key:

            

        if key & 0xFF == ord('c'): #Clear Image Completely
            img = cv2.imread(path)


        elif key & 0xFF == ord('z'): #Undo Change
            undoImg()
            

        elif key & 0xFF == ord('l'): #Legan Method Mode
            print("Legan Mode Activated")
            leganMode()
            

        elif key & 0xFF == ord('s'): #Silver Method Mode
            print("Silver Mode Activated")
            silverMode()
       
        
        elif key & 0xFF == ord('g'): #Goode's Method Mode
            print("Goode's Mode Activated")
            goodeMode()

        elif key & 0xFF == ord('m'): #Measuring Mode
            print("Measuring Mode Activated")
            measuringMode()

        elif key & 0xFF == ord('d'): #Distance Calibration Method Mode
            print("Distance Calibration Mode Activated")
            calibrationMode()

        elif key & 0xFF == ord('e'): #Exit Program
            
            print("Do you want to save the current image?(Y/N)")
            key = cv2.waitKey(0)
            if key & 0xFF == ord('y'):
                #Get Current time and format it to get unique folder name
                currentTime = datetime.now()
                folderName = currentTime.strftime("%d-%m-%Y %H;%M")
                folderPath = "Saved Images/"+folderName

                #Create new folder
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)
                
                newImagePath = "Saved Images/"+folderName+"/image.jpg"
                cv2.imwrite(newImagePath,img)
                
                
            elif key & 0xFF == ord('n'):
                pass

            else:
                continue 

            print("Do you want to save the cached images?(Y/N)")
            key = cv2.waitKey(0)
            if key & 0xFF == ord('y'):
                #Get Current time and format it to get unique folder name
                currentTime = datetime.now()
                folderName = currentTime.strftime("%d-%m-%Y %H;%M")
                folderPath = "Cached Images/"+folderName

                #Create new folder
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)
                
                #Loop over current cached images, move them to new folder and delete them from cache
                i = 0
                while i < currentImgCount+1:
                    imagePath = "cache/image"+str(i)+".jpg"
                    newImagePath = "Cached Images/"+folderName+"/image"+str(i)+".jpg"
                    os.rename(imagePath,newImagePath)
                    i+=1
                exit()
            elif key & 0xFF == ord('n'):
                #Remove all images in cache
                i = 0
                while i < currentImgCount:
                    imagePath = "cache/image"+str(i)+".jpg"
                    os.remove(imagePath)
                    i+=1
                exit()
        
                
            
    
    