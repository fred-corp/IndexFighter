import numpy as np
import time
from threading import Thread, Lock

class DynamicsHandler:
  def __init__(self, fieldShape, friction, borderX, borderY, player1, player2, coordsPuck):
    self.fieldShape = fieldShape
    self.player1 = player1
    self.player2 = player2
    self.coordsPuck = coordsPuck
    self.friction = friction
    self.borderX = borderX
    self.borderY = borderY
    self.stopped = True
    self.prevTime = time.time()
    self.lock = Lock()
    self.doPlayer1Collide = True
    self.doPlayer2Collide = True
    self.doFriction = False
    self.bounce1 = False
    self.bounce2 = False
  
  def start(self):
    self.stopped = False
    self.thread = Thread(target=self.calcPuckCoord, args=())
    self.thread.start()
    return self

  def stop(self):
    self.stopped = True

  def enableCollisions(self, player1=True, player2=True):
    self.doPlayer1Collide = player1
    self.doPlayer2Collide = player2

  def updatePlayerCoords(self, player1, player2):
    self.player1 = player1
    self.player2 = player2

  def calcPuckCoord(self):
    while not self.stopped:
      # Calculate the time difference
      currTime = time.time()
      timeDiff = currTime - self.prevTime
      self.prevTime = currTime
      with self.lock:
        puckSpeed = self.coordsPuck[2] # in px/s
        puckAngle = self.coordsPuck[3] # in rad
        puckCoords = self.coordsPuck[0]
        puckSize = self.coordsPuck[1]

      # Calculate the new Puck Coords
      newPuckCoords = [puckCoords[0] + puckSpeed*timeDiff * np.cos(puckAngle), puckCoords[1] + puckSpeed*timeDiff * np.sin(puckAngle)]
      
      

      # Calculate the new Puck Angle on bounce with border, considering the puck size
      if newPuckCoords[0] - puckSize < self.borderX or newPuckCoords[0] + puckSize > self.fieldShape[1] - self.borderX:
        puckAngle = np.pi - puckAngle
        # If the puck is inside the border, move it to the border
        if newPuckCoords[0] - puckSize < self.borderX:
          newPuckCoords[0] = self.borderX + puckSize
        elif newPuckCoords[0] + puckSize > self.fieldShape[1] - self.borderX:
          newPuckCoords[0] = self.fieldShape[1] - self.borderX - puckSize
      if newPuckCoords[1] - puckSize < self.borderY or newPuckCoords[1] + puckSize > self.fieldShape[0] - self.borderY:
        puckAngle = -puckAngle
        # If the puck is inside the border, move it to the border
        if newPuckCoords[1] - puckSize < self.borderY:
          newPuckCoords[1] = self.borderY + puckSize
        elif newPuckCoords[1] + puckSize > self.fieldShape[0] - self.borderY:
          newPuckCoords[1] = self.fieldShape[0] - self.borderY - puckSize

      if self.doPlayer1Collide:
        # Calculate the new Puck Angle on bounce with player 1 position and angle, considering the puck size
        # TODO: Solve collision issue (collision is sometimes not detected)
        player1StartCoord = [self.player1.coordX, self.player1.coordY]
        player1Angle = self.player1.angle
        x1 = int(player1StartCoord[0] + self.player1.size * np.cos(player1Angle))
        y1 = int(player1StartCoord[1] + self.player1.size * np.sin(player1Angle))
        if x1 == player1StartCoord[0]:
          x1 += 1
        player1EndCoord = [x1, y1]

        # calculate the distance between the puck and the line between the player
        dist = np.abs(((newPuckCoords[0] - player1StartCoord[0]) * (player1EndCoord[1] - player1StartCoord[1])) - ((newPuckCoords[1] - player1StartCoord[1]) * (player1EndCoord[0] - player1StartCoord[0])) / np.sqrt((player1EndCoord[1] - player1StartCoord[1])**2 + (player1EndCoord[0] - player1StartCoord[0])**2))
        
        # if the puck coords gets between the player coords with a tolerance of the ball radius, bounce
        if dist <= puckSize and not self.bounce1:
          # Calculate the new Puck Angle
          puckAngle = 2 * player1Angle - puckAngle
          self.bounce1 = True
        elif dist > puckSize and self.bounce1:
          self.bounce1 = False

        # TODO:[Future version] Calculate the new Puck Speed (considering the player speed)

      if self.doPlayer2Collide:
        # Calculate the new Puck Angle on bounce with player 2 position and angle, considering the puck size
        # TODO: Solve collision issue (collision is sometimes not detected)
        player2StartCoord = [self.player2.coordX, self.player2.coordY]
        player2Angle = self.player2.angle
        x2 = int(player2StartCoord[0] - self.player2.size * np.cos(player2Angle))
        y2 = int(player2StartCoord[1] - self.player2.size * np.sin(player2Angle))
        if x2 == player2StartCoord[0]:
          x2 += 1
        player2EndCoord = [x2, y2]

        # calculate the distance between the puck and the line between the player
        dist = np.abs(((newPuckCoords[0] - player2StartCoord[0]) * (player2EndCoord[1] - player2StartCoord[1])) - ((newPuckCoords[1] - player2StartCoord[1]) * (player2EndCoord[0] - player2StartCoord[0])) / np.sqrt((player2EndCoord[1] - player2StartCoord[1])**2 + (player2EndCoord[0] - player2StartCoord[0])**2))

        # if the puck coords gets between the player coords with a tolerance of the ball radius, bounce
        if dist <= puckSize and not self.bounce2:
          # Calculate the new Puck Angle
          puckAngle = 2 * player2Angle - puckAngle
          self.bounce2 = True
        elif dist > puckSize and self.bounce2:
          self.bounce2 = False

        # TODO:[Future version] Calculate the new Puck Speed

      if self.doFriction:
        # TODO:[Future version] Calculate the new Puck Speed with friction
        # Calculate the new Puck Speed with time difference and friction
        puckSpeed /= self.friction ## timeDiff
        if puckSpeed < 1:
          puckSpeed = 0
      # Update the puck coords, speed and angle
      with self.lock:
        self.coordsPuck[0] = newPuckCoords
        self.coordsPuck[2] = int(puckSpeed)
        self.coordsPuck[3] = puckAngle
      time.sleep(0.001)

  def getPuckCoords(self):
    # convert the coords to int
    with self.lock:
      puckCoords = [int(self.coordsPuck[0][0]), int(self.coordsPuck[0][1])]
      return [puckCoords, self.coordsPuck[1], self.coordsPuck[2], self.coordsPuck[3]]


if __name__ == "__main__":
  print("Dynamics handler for IndexFighter")
  print("Nothing to do here !")