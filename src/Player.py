import numpy as np

class Player :
  def __init__(self):
    self.coordX = 0
    self.coordY = 0
    self.angle = 0
    self.size = 80
    self.score = 0
    self.service = False
  
  def setParams(self, coordPlayer):
    self.coordX = coordPlayer[0][0]
    self.coordY = coordPlayer[0][1]
    self.angle = coordPlayer[1]
    self.size = coordPlayer[2]
  
  def getParams(self):
    return [[self.coordX, self.coordY], self.angle, self.size]
