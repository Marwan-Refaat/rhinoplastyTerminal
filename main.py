from cv2 import cv2 
import math
import sympy
import os
from datetime import datetime

path = "angleTest.png"
img = cv2.imread(path)

currentMode = 0
currentImgCount = 0


def updateCounter(num):
    global currentImgCount

    if num == 1:
        currentImgCount+=1
    elif num == -1:
        currentImgCount-=1


def drawCircles(event,x,y,flags,params):
    pointsList = params[0] 
    if (event == cv2.EVENT_LBUTTONDOWN) and (len(pointsList) < 4) : #Left Click and <4 points exist
        
        #Draw Point
        cv2.circle(img,(x,y),2,(0,0,255),cv2.FILLED)
        
        #Add to points list
        pointsList.append((x,y))
        print("Point drawn at:"+str(x) +"," + str(y))
        print(pointsList)

        
        if len(pointsList) == 2:#If 2 points drawn
            #Draw Line between first two points
            cv2.line(img,pointsList[0],pointsList[1],(0,0,255),2)

        elif len(pointsList) == 4:#If 4 points drawn
            #Draw Line between last two points
            cv2.line(img,pointsList[2],pointsList[3],(0,0,255),2)

            #Get angle between two lines
            l1 = sympy.Line(pointsList[0],pointsList[1])
            l2 = sympy.Line(pointsList[2],pointsList[3])
            
            #Print angle in degrees
            print(math.degrees(l1.smallest_angle_between(l2)))

def leganMode():
    global img
    pointsList = []

    imagePath = "cache/image"+str(currentImgCount)+".jpg"
    updateCounter(1)

    cv2.imwrite(imagePath,img)
    while True:
        cv2.imshow('Image',img)

        cv2.setMouseCallback('Image',drawCircles,[pointsList])

        if (cv2.waitKey(1) & 0xFF == ord('e') or len(pointsList) >= 5): #Exit Current Mode
            print("Do you want to save these changes?(Y/N)")
            key = cv2.waitKey(0)
            if key & 0xFF == ord('y'):
                break
            elif key & 0xFF == ord('n'):
                img = cv2.imread(imagePath)
                os.remove(imagePath)
                updateCounter(-1)
                break
            else:
                print("Do you want to save these changes?(Y/N)")
                key = cv2.waitKey(0)





while True:
    cv2.imshow('Image',img)
    print("Begin Input Mode")
    print("------LEGEND------")
    print("C - Clear Image Completely")
    print("Z - Undo Last Image Modification")
    print("L - Legan's Method Mode")
    print("S - Silver's Method Mode")
    print("G - Goode's Method Mode")
    print("M - Measuring Mode")
    print("E - Exit Program")
    key = cv2.waitKey(0)
    #cmd = input("Enter Command: ")
    if key:

            

        if key & 0xFF == ord('c'): #Clear Image Completely
            img = cv2.imread(path)


        elif key & 0xFF == ord('z'): #Undo Change
            newPath = "/cache/"+str(currentImgCount)+".jpg"
            img = cv2.imread(newPath)
            currentImgCount-=1

        elif key & 0xFF == ord('l'): #Legan Method Mode
            print("Legan Mode Activated")
            leganMode()
            

        elif key & 0xFF == ord('s'): #Silver Method Mode
            print("Silver Mode Activated")
            #time.sleep(3)
        # lineMode()
        
        elif key & 0xFF == ord('g'): #Goode's Method Mode
            print("Goode's Mode Activated")
        # lineMode()

        elif key & 0xFF == ord('m'): #Measuring Mode
            print("Measuring Mode Activated")

        elif key & 0xFF == ord('e'): #Exit Program
            print("Do you want to save the cached images?(Y/N)")
            key = cv2.waitKey(0)
            if key & 0xFF == ord('y'):
                #Get Current time and format it to get unique folder name
                currentTime = datetime.now()
                folderName = currentTime.strftime("%d-%m-%Y %H;%M")
                folderPath = "Saved Images/"+folderName

                #Create new folder
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)
                
                #Loop over current cached images, move them to new folder and delete them from cache
                i = 0
                while i < currentImgCount+1:
                    imagePath = "cache/image"+str(i)+".jpg"
                    newImagePath = "Saved Images/"+folderName+"/image"+str(i)+".jpg"
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
        
                
            
    
    