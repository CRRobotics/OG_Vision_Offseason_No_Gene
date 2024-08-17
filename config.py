#import cv2
#import os
import math

possibleColors = ["Green", "Blue", "Red", "Yellow", "Orange"]
possibleShapes = ["Diamond", "Hexagon"]


topOfScreenCoord = 639
bottomOfScreenCoord = -639
rightOfScreenCoord = 639
leftOfScreenCoord = -639

#probably need to test everything somehow, and look into fixing the stuff i commented on 

class Finger:
    def __init__(self, color):
        self.xCoord = 639
        self.yCooord = 639
        self.alive = True
        self.color = color # potentially need to have a list of colors and throw an exception if it's not an accepted color
        
    # accessors 
    def getCoords(self):
        return (self.xCoord, self.yCoord)
        
    def getXCoord(self):
        return self.xCoord
        
    def getYCoord(self):
        return self.yCoord
        
    def isAlive(self):
        return self.alive
    
    def getColor(self):
        return self.color
        
    # mutators
    def setXCoord(self, xCoord):
        self.xCoord = xCoord
        
    def setYCoord(self, yCoord):
        self.yCoord = yCoord
        
    def changeXCoord(self, change):
        self.xCoord += change
        
    def changeYCoord(self, change):
        self.yCoord += change
        
    def retrieveCoordsFromAI(self):
        pass
    
    def move(self):
        pass



class Enemy:
    def __init__(self, color):
        self.xCoord = 639
        self.yCoord = 639
        self.color = color
        self.shape = shape
        
    # accessors
    def getCoords(self):
        return (self.xCoord, self.yCoord)
        
    def getXCoord(self):
        return self.xCoord
        
    def getYCoord(self):
        return self.yCoord
        
    def getColor(self):
        return self.color
        
    def getShape(self):
        return self.shape
        
    # mutators
    def setXCoord(self, xCoord):
        self.xCoord = xCoord
        
    def setYCoord(self, yCoord):
        self.yCoord = yCoord
        
    def changeXCoord(self, change):
        self.xCoord += change
        
    def changeYCoord(self, change):
        self.yCoord += change
        
        
        
class Hexagon(Enemy):
    def __init__(self, color):
        Enemy.__init__(color, "Hexagon")
    
    def findClosestEnemy(self, fingers): #this is probably not the best way to do this
        lowestDistance = 639000
        closestFinger = fingers[0]
        for finger in fingers:
            xCoord = finger.getXCoord()
            yCoord = finger.getYCoord()
            distance = (xCoord ** 2 + yCoord ** 2) ** (1/2)
            if lowestDistance > distance:
                lowestDistance = distance
                closestFinger = finger
        return closestFinger
                
    def move(self, fingers): #can fingers not be a parameter here, cause it feels like it could
        finger = self.findClosestEnemy(fingers)
        xDistance = self.getXCoord() - finger.getXCoord()
        yDistance = self.getYCoord() - finger.getYCoord()
        hypotenuse = (xDistance ** 2 + yDistance ** 2) ** (1/2)
        xChange = xDistance / hypotenuse
        yChange = yDistance / hypotenuse
        self.changeXCoord(xChange)
        self.changeYCoord(yChange)
    
    
    
class Diamond(Enemy):
    def __init__(self, color):
        Enemy.__init__(color, "Diamond")
        self.direction = 0
    
    def atEdge(self):
        if self.getCoords()[0] == rightOfScreenCoord or self.getCoords()[0] == leftOfScreenCoord:
            self.direction = 180 - self.direction 
        elif self.getCoords()[1] == bottomOfScreenCoord or self.getCoords()[1] == topOfScreenCoord:
            self.direction *= -1
            
    def move(self): # might get out of bounds and so not turn and be unable to move and everything breaks
        self.atEdge()
        self.changeXCoord(math.acos(direction * math.pi / 180))
        self.changeYCoord(math.asin(direction * math.pi / 180))
        

def summonEnemies():
    pass
        
        
def main():
    fingers = [Finger("Blue") for i in range(5)]
    print("hi")
    enemies = []
    while True:
        for finger in fingers:
            finger.retrieveCoordsFromAI()
            finger.move()
        for enemie in enemies:
            enemie.move()
        
    
    
main()
