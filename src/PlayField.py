import cv2
import numpy as np

class PlayField:
  def __init__(self, fieldShape, borderX, borderY):
    self.borderX = borderX
    self.borderY = borderY
    self.borderColor = (255, 255, 255)
    self.puckVectorThickness = 2
    self.fieldShape = fieldShape
    self.backGround = self.generateBackGround()

  def getField(self, coordsPlayer1, coordsPlayer2, coordsPuck, drawPlayers=True, drawPlayerVector=True, drawPuck = True, drawPuckVector = True):
    black = self.backGround.copy()
    
    if drawPlayers:
      # Draw a line of thickness 5 and length 60 with the same starting point
      # as the 1st coord of player 1, and same angle as the coords of player 1 on the black
      P1angle = coordsPlayer1[3]
      cv2.line(black, tuple(coordsPlayer1[0]), tuple(coordsPlayer1[1]), (0, 255, 0), 5)

      # Draw a line of thickness 5 and length 60 with the same starting point
      # as the 1st coord of player 2, and same angle as the coords of player 2 on the black
      P2angle = coordsPlayer2[3]
      cv2.line(black, tuple(coordsPlayer2[0]), tuple(coordsPlayer2[1]), (0, 0, 255), 5)

    if drawPlayerVector:
      # Draw a line of thickness 2 and length 40 in the middle the 1st coord and endCoord of player 1 on the black,
      # Perpendicular to the line between the 1st coord and endCoord of player 1
      P1angle = coordsPlayer1[3]
      vectorLength = 40
      # start coord between the 1st coord and endCoord of player 1
      startCoord = [int((coordsPlayer1[0][0] + coordsPlayer1[1][0])/2), int((coordsPlayer1[0][1] + coordsPlayer1[1][1])/2)]
      endCoord = [int(startCoord[0] + vectorLength * np.cos(P1angle - np.pi/2)), int(startCoord[1] + vectorLength * np.sin(P1angle - np.pi/2))]
      cv2.line(black, tuple(startCoord), tuple(endCoord), (0, 255, 0), self.puckVectorThickness)

      # Draw a line of thickness 2 and length 40 between the 1st coord and endCoord of player 2 on the black
      P2angle = coordsPlayer2[3]
      vectorLength = 40
      # start coord between the 1st coord and endCoord of player 2
      startCoord = [int((coordsPlayer2[0][0] + coordsPlayer2[1][0])/2), int((coordsPlayer2[0][1] + coordsPlayer2[1][1])/2)]
      endCoord = [int(startCoord[0] + vectorLength * np.cos(P2angle - np.pi/2)), int(startCoord[1] + vectorLength * np.sin(P2angle - np.pi/2))]
      cv2.line(black, tuple(startCoord), tuple(endCoord), (0, 0, 255), self.puckVectorThickness)

    if drawPuck:
      # Draw the Puck on the black rectangle
      puckSize = coordsPuck[1]
      puckColor = (255, 255, 0)
      # Convert the coords to int, because the circle function needs int
      coordsPuck[0] = [int(coordsPuck[0][0]), int(coordsPuck[0][1])]
      cv2.circle(black, tuple(coordsPuck[0]), puckSize, puckColor, -1)
    
    if drawPuckVector:
      # Draw the Puck Vector on the black rectangle
      puckVectorColor = (0, 0, 255)
      puckSpeed = coordsPuck[2]
      puckAngle = coordsPuck[3]
      if puckSpeed > 0:
        # Calculate the end coord of the puck vector
        endCoord = [int(coordsPuck[0][0] + puckSpeed * np.cos(puckAngle)), int(coordsPuck[0][1] + puckSpeed * np.sin(puckAngle))]
        coordsPuck[0] = [int(coordsPuck[0][0]), int(coordsPuck[0][1])]
        cv2.line(black, tuple(coordsPuck[0]), tuple(endCoord), puckVectorColor, self.puckVectorThickness)

    return black

  def generateBackGround(self):
    # Create a black rectangle with the same size as the image
    # to draw the text on
    black = np.zeros((self.fieldShape[0], self.fieldShape[1], 3), np.uint8)
    # Draw a N px wide white border around the black rectangle
    black[:] = self.borderColor
    black[self.borderY:-self.borderY, self.borderX:-self.borderX] = (0, 0, 0)

    # Draw a blue rectangle of width 4 in the middle of the black rectangle
    cv2.rectangle(black, (self.fieldShape[1]//2-2, 0), (self.fieldShape[1]//2+2, self.fieldShape[0]), (255, 0, 0), 4)
    return black

