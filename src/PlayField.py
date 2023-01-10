import cv2
import numpy as np

class PlayField:
  def __init__(self, fieldShape, borderX, borderY, goalHeight):
    self.borderX = borderX
    self.borderY = borderY
    self.borderColor = (255, 255, 255)
    self.puckVectorThickness = 2
    self.fieldShape = fieldShape
    self.goalHeight = goalHeight
    self.backGroundColor = (38, 38, 38)
    self.backGround = self.generateBackGround()

  def getField(self, player1, player2, coordsPuck, drawScore = True, drawPlayers=True, drawPlayerVector=False, drawPuck = True, drawPuckVector = False):
    black = self.backGround.copy()

    coordsPlayer1 = player1.getParams()
    coordsPlayer2 = player2.getParams()
    
    if drawScore:
      # Draw the score
      cv2.putText(black, str(player1.score), (int(self.fieldShape[1]/2 - 100), 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)
      cv2.putText(black, str(player2.score), (int(self.fieldShape[1]/2 + 100), 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)

    if drawPlayers:
      # Draw a line of thickness 5 and length 60 with the same starting point
      # as the 1st coord of player 1, and same angle as the coords of player 1 on the black
      P1angle = coordsPlayer1[1]
      x1 = int(coordsPlayer1[0][0] + coordsPlayer1[2] * np.cos(P1angle))
      y1 = int(coordsPlayer1[0][1] + coordsPlayer1[2] * np.sin(P1angle))
      cv2.line(black, tuple(coordsPlayer1[0]), (x1, y1), (0, 255, 0), 5)

      # Draw a line of thickness 5 and length 60 with the same starting point
      # as the 1st coord of player 2, and same angle as the coords of player 2 on the black
      P2angle = coordsPlayer2[1]
      x2 = int(coordsPlayer2[0][0] - coordsPlayer2[2] * np.cos(P2angle))
      y2 = int(coordsPlayer2[0][1] - coordsPlayer2[2] * np.sin(P2angle))
      cv2.line(black, tuple(coordsPlayer2[0]), (x2, y2), (0, 0, 255), 5)

    if drawPlayerVector and drawPlayers:
      # Draw a line of thickness 2 and length 40 in the middle the 1st coord and endCoord of player 1 on the black,
      # Perpendicular to the line between the 1st coord and endCoord of player 1
      vectorLength = 40
      # start coord between the 1st coord and endCoord of player 1
      startCoord = [int((coordsPlayer1[0][0] + x1)/2), int((coordsPlayer1[0][1] + y1)/2)]
      endCoord = [int(startCoord[0] + vectorLength * np.cos(P1angle - np.pi/2)), int(startCoord[1] + vectorLength * np.sin(P1angle - np.pi/2))]
      cv2.line(black, tuple(startCoord), tuple(endCoord), (0, 255, 0), self.puckVectorThickness)

      # Draw a line of thickness 2 and length 40 between the 1st coord and endCoord of player 2 on the black
      vectorLength = 40
      # start coord between the 1st coord and endCoord of player 2
      startCoord = [int((coordsPlayer2[0][0] + x2)/2), int((coordsPlayer2[0][1] + y2)/2)]
      endCoord = [int(startCoord[0] + vectorLength * np.cos(P2angle - np.pi/2)), int(startCoord[1] + vectorLength * np.sin(P2angle - np.pi/2))]
      cv2.line(black, tuple(startCoord), tuple(endCoord), (0, 0, 255), self.puckVectorThickness)

    if drawPuck:
      # Draw the Puck on the black rectangle
      puckSize = coordsPuck[1]
      puckColor = (255, 255, 0)
      # Convert the coords to int, because the circle function needs int
      coordsPuck[0] = [int(coordsPuck[0][0]), int(coordsPuck[0][1])]
      cv2.circle(black, tuple(coordsPuck[0]), puckSize, puckColor, -1)
    
    if drawPuckVector and drawPuck:
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
    black[self.borderY:-self.borderY, self.borderX:-self.borderX] = self.backGroundColor

    # Draw a blue rectangle of width 4 in the middle of the black rectangle inside of the borderY
    cv2.rectangle(black, (int(self.fieldShape[1]/2 - 2), self.borderY), (int(self.fieldShape[1]/2 + 2), self.fieldShape[0] - self.borderY - 1), (255, 0, 0), -1)

    # Draw the goals on each side of the field
    goalWidth = 5
    goalColor = (0, 127, 255)
    # Draw the left goal
    cv2.rectangle(black, (self.borderX, int(self.fieldShape[0]/2 - self.goalHeight/2)), (self.borderX - goalWidth, int(self.fieldShape[0]/2 + self.goalHeight/2)), goalColor, -1)
    # Draw the right goal
    cv2.rectangle(black, (self.fieldShape[1] - self.borderX + goalWidth, int(self.fieldShape[0]/2 - self.goalHeight/2)), (self.fieldShape[1] - self.borderX, int(self.fieldShape[0]/2 + self.goalHeight/2)), goalColor, -1)
    return black


if __name__ == "__main__":
  print("Playfield utils for IndexFighter")
  print("Nothing to do here !")