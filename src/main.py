import cv2
import numpy as np
import time
import mediapipe as mp
import sys
from threading import Thread, Lock

cam = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


imShape = (720, 1280)

camLock = Lock()
dynLock = Lock()


class CameraHandler:
  def __init__(self, fieldShape):
    self.cam = cv2.VideoCapture(0)
    self.imShape = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH), self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    self.mp_drawing = mp.solutions.drawing_utils
    self.mp_drawing_styles = mp.solutions.drawing_styles
    self.mp_hands = mp.solutions.hands
    self.stopped = True
    self.coordsPlayer1 = [[1, 2], [3, 4], 80, 0]
    self.coordsPlayer2 = [[1279, 2], [1277, 4], 80, 0]
    self.image = np.zeros((int(self.imShape[0]), int(self.imShape[1]), 3), np.uint8)
    self.fieldShape = fieldShape

  def start(self):
    if not self.stopped:
      return
    self.stopped = False
    Thread(target=self.update, args=()).start()
    return self

  def update(self):
    while True:
      if self.stopped:

        return

      coordsPlayer1 = self.coordsPlayer1
      coordsPlayer2 = self.coordsPlayer2
      pTime = 0
      cTime = 0

      x1p1 = coordsPlayer1[0][0]
      y1p1 = coordsPlayer1[0][1]
      x2p1 = coordsPlayer1[1][0]
      y2p1 = coordsPlayer1[1][1]
      x1p2 = coordsPlayer2[0][0]
      y1p2 = coordsPlayer2[0][1]
      x2p2 = coordsPlayer2[1][0]
      y2p2 = coordsPlayer2[1][1]

      with mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
        while cam.isOpened():
          if self.stopped:
            cv2.destroyAllWindows()
            cam.release()
            return

          success, image = cam.read()
          if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
          # mirror image
          image = cv2.flip(image, 1)
          # To improve performance, optionally mark the image as not writeable to
          # pass by reference.
          image.flags.writeable = False
          image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          results = hands.process(image)

          # Draw the hand annotations on the image.
          image.flags.writeable = True
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

          _coordsPlayer1 = self.coordsPlayer1
          _coordsPlayer2 = self.coordsPlayer2
          if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
              mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())


              for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8:
                  if cx < imShape[1]/2:
                    x1p1 = cx
                    y1p1 = cy
                  else:
                    x1p2 = cx
                    y1p2 = cy
                if id == 5:
                  if cx < imShape[1]/2:
                    x2p1 = cx
                    y2p1 = cy
                  else:
                    x2p2 = cx
                    y2p2 = cy
            
            # Adjust P1 and P2 coords to fit in the field if the image shape is different than the field shape
            imageShape = image.shape
            if imageShape[1] != self.fieldShape[1] or imageShape[0] != self.fieldShape[0]:
              x1p1 = int(x1p1 * self.fieldShape[1] / imShape[1])
              y1p1 = int(y1p1 * self.fieldShape[0] / imShape[0])
              x2p1 = int(x2p1 * self.fieldShape[1] / imShape[1])
              y2p1 = int(y2p1 * self.fieldShape[0] / imShape[0])
              x1p2 = int(x1p2 * self.fieldShape[1] / imShape[1])
              y1p2 = int(y1p2 * self.fieldShape[0] / imShape[0])
              x2p2 = int(x2p2 * self.fieldShape[1] / imShape[1])
              y2p2 = int(y2p2 * self.fieldShape[0] / imShape[0])


            # Calculate P1 angle
            if x1p1 != x2p1:
              P1angle = np.arctan((y2p1 - y1p1) / (x2p1 - x1p1))
            else:
              P1angle = 0
            if x2p1 < x1p1:
              P1angle += np.pi
            x2 = int(_coordsPlayer1[0][0] + np.cos(P1angle) * self.coordsPlayer1[2])
            y2 = int(_coordsPlayer1[0][1] + np.sin(P1angle) * self.coordsPlayer1[2])
            coordsPlayer1 = [[x1p1, y1p1], [x2, y2], self.coordsPlayer1[2], P1angle]

            # Calculate P2 angle
            if x1p2 != x2p2:
              P2angle = np.arctan((y2p2 - y1p2) / (x2p2 - x1p2))
            else:
              P2angle = 0
            if x2p2 < x1p2:
              P2angle += np.pi
            x2 = int(_coordsPlayer2[0][0] + np.cos(P2angle) * self.coordsPlayer2[2])
            y2 = int(_coordsPlayer2[0][1] + np.sin(P2angle) * self.coordsPlayer2[2])
            coordsPlayer2 = [[x1p2, y1p2], [x2, y2], self.coordsPlayer2[2], P2angle]

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            with camLock:
              self.coordsPlayer1 = coordsPlayer1
              self.coordsPlayer2 = coordsPlayer2
              self.image = image


  def stop(self):
    self.stopped = True

  def isStopped(self):
    return self.stopped

  def getCoords(self):
    return self.coordsPlayer1, self.coordsPlayer2

  def getImage(self):
    return self.image

class PlayField:
  def __init__(self, borderX, borderY):
    self.borderX = borderX
    self.borderY = borderY
    self.borderColor = (255, 255, 255)
    self.puckVectorThickness = 2

  def getField(self, coordsPlayer1, coordsPlayer2, coordsPuck, drawPlayers=True, drawPlayerVector=True, drawPuck = True, drawPuckVector = True):
    # Create a black rectangle with the same size as the image
    # to draw the text on
    black = np.zeros((imShape[0], imShape[1], 3), np.uint8)


    # Draw a N px wide white border around the black rectangle
    black[:] = self.borderColor
    black[self.borderY:-self.borderY, self.borderX:-self.borderX] = (0, 0, 0)

    # Draw a blue rectangle of width 4 in the middle of the black rectangle
    cv2.rectangle(black, (imShape[1]//2-2, 0), (imShape[1]//2+2, imShape[0]), (255, 0, 0), 4)

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


class DynamicsHandler:
  def __init__(self, friction, borderX, borderY, coordsPlayer1, coordsPlayer2, coordsPuck):
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
      if newPuckCoords[0] - puckSize < self.borderX or newPuckCoords[0] + puckSize > imShape[1] - self.borderX:
        puckAngle = np.pi - puckAngle
      if newPuckCoords[1] - puckSize < self.borderY or newPuckCoords[1] + puckSize > imShape[0] - self.borderY:
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
      with dynLock:
        self.coordsPuck[0] = newPuckCoords
        self.coordsPuck[2] = int(puckSpeed)
        self.coordsPuck[3] = puckAngle

  def getPuckCoords(self):
    # convert the coords to int
    puckCoords = [int(self.coordsPuck[0][0]), int(self.coordsPuck[0][1])]
    return [puckCoords, self.coordsPuck[1], self.coordsPuck[2], self.coordsPuck[3]]



def startGame(playerNum = 1):

  borderX = 80
  borderY = 50
  friction = 1
  imShape = (720, 1280)
  coordsPuck = [[640, 360], 20, 250, np.pi/4]

  camHandler = CameraHandler(imShape)
  camHandler.start()
  playField = PlayField(borderX, borderY)

  coordsPlayer1, coordsPlayer2 = camHandler.getCoords()
  dynamicsHandler = DynamicsHandler(friction, borderX, borderY, coordsPlayer1, coordsPlayer2, coordsPuck)
  dynamicsHandler.start()
  
  while True:
    coordsPlayer1, coordsPlayer2 = camHandler.getCoords()
    playfield = playField.getField(coordsPlayer1, coordsPlayer2, coordsPuck)
    dynamicsHandler.updatePlayerCoords(coordsPlayer1, coordsPlayer2)
    coordsPuck = dynamicsHandler.getPuckCoords()
    cv2.imshow("Image", camHandler.getImage())
    cv2.imshow("Playfield", playfield)
    ##time.sleep(0.001)
    if cv2.waitKey(1) == 27:
      camHandler.stop()
      dynamicsHandler.stop()
      cv2.destroyAllWindows()
      break



if __name__ == '__main__':

  startGame(sys.argv[1] if len(sys.argv) > 1 else 1)
  print("Done")