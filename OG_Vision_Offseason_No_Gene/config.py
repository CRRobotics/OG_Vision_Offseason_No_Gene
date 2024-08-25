#import cv2
#import os
import math
from random import randint
from time import sleep




topOfScreenCoord = 0
bottomOfScreenCoord = 479
rightOfScreenCoord = 639 # Actually correct
leftOfScreenCoord = 0




chanceOfSpawningEnemy = 9 # meaning one in ten chance
chanceOfHexagon = 2 # meaning one in 3




hexagonRadius = 639
diamondRadius = 639
circleRadius = 639




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
    
    def die(self):
        self.alive = False
    
    def move(self):
        pass
    
    # game methods
    def drawYourself(self):
        pass
    
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
       self.xCoord = 639
       self.yCoord = 639
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
       Enemy.__init__(color, "Hexagon", xCoord, yCoord)
  
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
       xDistance = self.getXCoord() - finger.getXCoord()
       yDistance = self.getYCoord() - finger.getYCoord()
       hypotenuse = math.sqrt(xDistance ** 2 + yDistance ** 2)
       xChange = xDistance / hypotenuse
       yChange = yDistance / hypotenuse
       self.changeXCoord(xChange)
       self.changeYCoord(yChange)
  
   def drawYourself(self):
       pass




  
  
  
class Diamond(Enemy):
   def __init__(self, color, xCoord, yCoord, direction):
       Enemy.__init__(color, "Diamond")
       self.direction = direction
  
   def atEdge(self):
       if self.getCoords()[0] == rightOfScreenCoord or self.getCoords()[0] == leftOfScreenCoord:
           self.direction = 180 - self.direction
       elif self.getCoords()[1] == bottomOfScreenCoord or self.getCoords()[1] == topOfScreenCoord:
           self.direction *= -1
          
   def move(self): # might get out of bounds and so not turn and be unable to move and everything breaks
       self.atEdge()
       self.changeXCoord(math.acos(self.alivedirection * math.pi / 180))
       self.changeYCoord(math.asin(self.direction * math.pi / 180))
      
   def drawYourself(self):
       pass




















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
       color = "Red"
       if colorNum == 1:
           color = "Orange"
       elif colorNum == 2:
           color = "Yellow"
       elif colorNum == 3:
           color = "Green"
       elif colorNum == 4:
           color = "Blue"
       xCoord = randint(0, rightOfScreenCoord)
       yCoord = randint(0, bottomOfScreenCoord)
      
       if randint(0, chanceOfHexagon) == 0:
           tempEnemie = Hexagon(color, xCoord, yCoord)
           enemies.append(tempEnemie)
       else:
           direction = randint(0, 359)
           tempEnemie = Diamond(color, xCoord, yCoord, direction)
           enemies.append(tempEnemie)




def gameOver():
   pass




def main():
   global stillAlive
   while stillAlive:
       summonEnemies()
       counter = 0
       for finger in fingers:
           finger.retrieveCoordsFromAI()
           finger.move()
           if finger.isAlive() == False:
               counter += 1
       if counter >= 5:
           stillAlive = False
       for enemie in enemies:
           enemie.move()
           enemies.drawYourself()
       sleep(.001)
   gameOver()
   print("hi. you do be dead though. So sad.")
  
#still need: way to have things die;
  
main()








