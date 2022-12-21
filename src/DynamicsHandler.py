import numpy as np
import time
from threading import Thread, Lock

class DynamicsHandler:
  def __init__(self, fieldShape, friction, borderX, borderY, coordsPlayer1, coordsPlayer2, coordsPuck):
    self.fieldShape = fieldShape
    self.coordsPlayer1 = coordsPlayer1
    self.coordsPlayer2 = coordsPlayer2
    self.prevCoordsPlayer1 = coordsPlayer1
    self.prevCoordsPlayer2 = coordsPlayer2
    self.coordsPuck = coordsPuck
    self.friction = friction
    self.borderX = borderX
    self.borderY = borderY
    self.stopped = True
    self.prevTime = time.time()
    self.lock = Lock()
  
  def start(self):
    self.stopped = False
    self.thread = Thread(target=self.calcPuckCoord, args=())
    self.thread.start()
    return self

  def stop(self):
    self.stopped = True

  def updatePlayerCoords(self, coordsPlayer1, coordsPlayer2):
    self.prevCoordsPlayer1 = self.coordsPlayer1
    self.prevCoordsPlayer2 = self.coordsPlayer2
    self.coordsPlayer1 = coordsPlayer1
    self.coordsPlayer2 = coordsPlayer2

  def calcPuckCoord(self):
    while not self.stopped:
      # Calculate the time difference
      currTime = time.time()
      timeDiff = currTime - self.prevTime
      self.prevTime = currTime
      puckSpeed = self.coordsPuck[2] # in px/s
      puckAngle = self.coordsPuck[3] # in rad
      puckCoords = self.coordsPuck[0]
      puckSize = self.coordsPuck[1]

      # Calculate the new Puck Coords
      newPuckCoords = [puckCoords[0] + puckSpeed*timeDiff * np.cos(puckAngle), puckCoords[1] + puckSpeed*timeDiff * np.sin(puckAngle)]
      
      # Calculate the new Puck Speed with time difference and friction
      puckSpeed /= self.friction ## timeDiff
      if puckSpeed < 1:
        puckSpeed = 0

      # Calculate the new Puck Angle on bounce with border, considering the puck size
      if newPuckCoords[0] - puckSize < self.borderX or newPuckCoords[0] + puckSize > self.fieldShape[1] - self.borderX:
        puckAngle = np.pi - puckAngle
      if newPuckCoords[1] - puckSize < self.borderY or newPuckCoords[1] + puckSize > self.fieldShape[0] - self.borderY:
        puckAngle = -puckAngle

      # Calculate the new Puck Angle on bounce with player 1 position and angle, considering the puck size
      player1StartCoord = self.coordsPlayer1[0]
      player1EndCoord = self.coordsPlayer1[1]
      player1Angle = self.coordsPlayer1[3]
      player1NormalAngle = player1Angle + np.pi/2
      if puckCoords[0] - puckSize < player1EndCoord[0] and puckCoords[0] + puckSize > player1StartCoord[0] and puckCoords[1] - puckSize < player1EndCoord[1] and puckCoords[1] + puckSize > player1StartCoord[1]:
        # Calculate the new Puck Angle
        puckAngle = -puckAngle + 2 * player1NormalAngle
        # TODO: Calculate the new Puck Speed

      # Calculate the new Puck Angle on bounce with player 2 position and angle, considering the puck size
      player2StartCoord = self.coordsPlayer2[0]
      player2EndCoord = self.coordsPlayer2[1]
      player2Angle = self.coordsPlayer2[3]
      player2NormalAngle = player2Angle - np.pi/2
      if puckCoords[0] - puckSize < player2EndCoord[0] and puckCoords[0] + puckSize > player2StartCoord[0] and puckCoords[1] - puckSize < player2EndCoord[1] and puckCoords[1] + puckSize > player2StartCoord[1]:
        # Calculate the new Puck Angle
        puckAngle = -puckAngle + 2 * player2NormalAngle
        # TODO: Calculate the new Puck Speed

      # Update the puck coords, speed and angle
      with self.lock:
        self.coordsPuck[0] = newPuckCoords
        self.coordsPuck[2] = int(puckSpeed)
        self.coordsPuck[3] = puckAngle

  def getPuckCoords(self):
    # convert the coords to int
    puckCoords = [int(self.coordsPuck[0][0]), int(self.coordsPuck[0][1])]
    return [puckCoords, self.coordsPuck[1], self.coordsPuck[2], self.coordsPuck[3]]
