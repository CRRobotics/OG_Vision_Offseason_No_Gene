import cv2
#import os
import numpy as np
import math
from random import randint
from time import sleep




topOfScreenCoord = 0
bottomOfScreenCoord = 479
rightOfScreenCoord = 639 # Actually correct
leftOfScreenCoord = 0




chanceOfSpawningEnemy = 100 # meaning one in 101 chance
chanceOfHexagon = 2 # meaning one in 3




hexagonRadius = 10
diamondRadius = 10
circleRadius = 2




colors = {
   "Red" : (255, 0, 0),
   "Orange" : (255, 165, 0),
   "Yellow" : (255, 25, 0),
   "Green" : (0, 255, 0),
   "Blue" : (0, 0, 255)
}




#probably need to test everything somehow, and look into fixing the stuff i commented on



class Finger:
    def __init__(self, color):
       self.xCoord = 639
       self.yCoord = 638
       self.alive = True
       self.color = colors[color] # potentially need to have a list of colors and throw an exception if it's not an accepted color
      
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
    
    def die(self):
        self.alive = False
    
    # game methods
    def drawYourself(self, frame):
        return cv2.circle(frame, (self.xCoord, self.yCoord), 0, self.color, circleRadius)
    
    def touchingEnemy(self, enemies):
        enemyXCoord = 0
        enemyYCoord = 0
        for enemy in enemies:
            enemyXCoord = enemy.getXCoord()
            enemyYCoord = enemy.getYCoord()
            if enemy.getShape() == "Hexagon":
                if math.sqrt((enemyXCoord - self.xCoord) ** 2 + (enemyYCoord - self.yCoord) ** 2) <= circleRadius + hexagonRadius and enemy.isAlive():
                    if self.color == enemy.color:
                        self.alive = False
                    else:   
                            enemy.alive = False
            else:
                if math.abs(self.xCoord - enemyXCoord) + math.abs(self.yCoord - enemyYCoord) <= diamondRadius + circleRadius * math.sqrt(2):
                    if self.color == enemy.color:
                        self.alive = False
                    else:
                        enemy.alive = False




           #potential glithc: finger is before enemie, and so might not have access to the methods and break things
  
  
  












class Enemy:
   def __init__(self, shape, color, xCoord, yCoord):
       self.xCoord = xCoord
       self.yCoord = yCoord
       self.color = color
       self.shape = shape
       self.alive = True
      
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
  
   def die(self):
       self.alive = False
      
   # game methods
   def drawYourself(self):
       pass




      
      
      
class Hexagon(Enemy):
   def __init__(self, color, xCoord, yCoord):
       Enemy.__init__(self, "Hexagon", color, xCoord, yCoord)
  
   def findClosestEnemy(self, fingers): #this is probably not the best way to do this
       lowestDistance = 639000
       closestFinger = fingers[0]
       for finger in fingers:
           xCoord = finger.getXCoord()
           yCoord = finger.getYCoord()
           distance = math.sqrt(xCoord ** 2 + yCoord ** 2)
           if lowestDistance > distance:
               lowestDistance = distance
               closestFinger = finger
       return closestFinger
              
   def move(self, fingers): #can fingers not be a parameter here, cause it feels like it could
       finger = self.findClosestEnemy(fingers)
       xDistance = finger.getXCoord() - self.getXCoord()
       yDistance = finger.getYCoord() - self.getYCoord()
       hypotenuse = math.sqrt(xDistance ** 2 + yDistance ** 2)
       if hypotenuse != 0:
        xChange = xDistance / hypotenuse
        yChange = yDistance / hypotenuse
       else:
           print("DEAATHTHTHT ITS DIVIDE BY ZERO")
       self.changeXCoord(xChange)
       self.changeYCoord(yChange)
  
   def drawYourself(self, frame):
    # Calculate the six vertices of the hexagon
    vertices = []
    for i in range(6):
        angle = 2 * np.pi / 6 * i
        x = int(self.xCoord + hexagonRadius * np.cos(angle))
        y = int(self.yCoord + hexagonRadius * np.sin(angle))
        vertices.append((x, y))

    # Convert vertices to a numpy array
    vertices = np.array(vertices, np.int32)
    vertices = vertices.reshape((-1, 1, 2))

    # Create a copy of the original frame to draw the filled hexagon
    overlay = frame.copy()

    # Fill the hexagon on the overlay
    cv2.fillPoly(overlay, [vertices], self.color)

    # Blend the overlay with the original frame using alpha transparency
    alpha = 0.5  # Set transparency level to 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Optionally, you can still draw the border
    cv2.polylines(frame, [vertices], isClosed=True, color=self.color, thickness=2)
       




  
  
  
class Diamond(Enemy):
   def __init__(self, color, xCoord, yCoord, direction):
       Enemy.__init__(self, "Diamond", color, xCoord, yCoord)
       self.direction = direction
  
   def atEdge(self):
       if self.getCoords()[0] >= rightOfScreenCoord or self.getCoords()[0] <= leftOfScreenCoord:
           self.direction = 180 - self.direction
       elif self.getCoords()[1] >= bottomOfScreenCoord or self.getCoords()[1] <= topOfScreenCoord:
           self.direction *= -1
          
   def move(self, fingers): # might get out of bounds and so not turn and be unable to move and everything breaks
       self.atEdge()
       self.changeXCoord(math.cos(self.direction * math.pi / 180))
       self.changeYCoord(math.sin(self.direction * math.pi / 180))
      
   def drawYourself(self, frame):
    # Calculate the four vertices of the diamond
    vertices = [
        (self.xCoord, self.yCoord - diamondRadius),  # Top
        (self.xCoord + diamondRadius, self.yCoord),  # Right
        (self.xCoord, self.yCoord + diamondRadius),  # Bottom
        (self.xCoord - diamondRadius, self.yCoord)   # Left
    ]

    # Convert vertices to a numpy array
    vertices = np.array(vertices, np.int32)
    vertices = vertices.reshape((-1, 1, 2))

    # Create a copy of the original frame to draw the filled diamond
    overlay = frame.copy()

    # Fill the diamond on the overlay
    cv2.fillPoly(overlay, [vertices], self.color)

    # Blend the overlay with the original frame using alpha transparency
    alpha = 0.5  # Set transparency level to 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Optionally, you can still draw the border
    cv2.polylines(frame, [vertices], isClosed=True, color=self.color, thickness=2)
























thumb = Finger("Red")
pointer = Finger("Orange")
middle = Finger("Yellow")
ring = Finger("Green")
pinkie = Finger("Blue")




fingers = [thumb, pointer, middle, ring, pinkie]
enemies = []




stillAlive = True




def summonEnemies():
   global enemies
   if randint(0, chanceOfSpawningEnemy) == 0:
       colorNum = randint(0, 4)
       color = colors["Red"]
       if colorNum == 1:
           color = colors["Orange"]
       elif colorNum == 2:
           color = colors["Yellow"]
       elif colorNum == 3:
           color = colors["Green"]
       elif colorNum == 4:
           color = colors["Blue"]
       temp = randint(0, 1)
       if randint(0, 1) == 0:
        xCoord = randint(0, rightOfScreenCoord)
        if randint(0, 1) == 0:
            yCoord = topOfScreenCoord
        else:
            yCoord = bottomOfScreenCoord
       else:
           yCoord = randint(0, bottomOfScreenCoord)
           if randint(0, 1) == 0:
            xCoord = leftOfScreenCoord
           else:
            xCoord = rightOfScreenCoord


      
       if randint(0, chanceOfHexagon) == 0:
           tempEnemie = Hexagon(color, xCoord, yCoord)
           enemies.append(tempEnemie)
       else:
           direction = randint(0, 359)
           tempEnemie = Diamond(color, xCoord, yCoord, direction)
           enemies.append(tempEnemie)









def config_main(frame, fingerXCoords, fingerYCoords):
    global stillAlive
    summonEnemies()
    counter = 0
    for i in range(len(fingers)):
        finger = fingers[i]
        finger.changeXCoord(fingerXCoords[i])
        finger.changeYCoord(fingerYCoords[i])
        finger.drawYourself(frame)
        if finger.isAlive() == False:
            counter += 1
    if counter >= 5:
        stillAlive = False
    for enemie in enemies:
        enemie.move(fingers)
        enemie.drawYourself(frame)
    sleep(.001)
    return stillAlive
  
#still need: way to have things die;
  









