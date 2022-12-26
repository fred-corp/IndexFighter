import cv2
import numpy as np
import time
import mediapipe as mp
from threading import Thread, Lock

class CameraHandler:
  def __init__(self, fieldShape, camNum=0):
    self.cam = cv2.VideoCapture(0)
    self.imShape = [1280, 720]
    self.mp_drawing = mp.solutions.drawing_utils
    self.mp_drawing_styles = mp.solutions.drawing_styles
    self.mp_hands = mp.solutions.hands
    self.cam = cam = cv2.VideoCapture(camNum)
    self.stopped = True
    self.coordsPlayer1 = [[1, 2], np.pi/4, 80]
    self.coordsPlayer2 = [[1279, 2], -np.pi/4, 80]
    self.image = np.zeros((int(self.imShape[0]), int(self.imShape[1]), 3), np.uint8)
    self.fieldShape = fieldShape
    self.camLock = Lock()

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

      with self.camLock:
        coordsPlayer1 = self.coordsPlayer1.copy()
        coordsPlayer2 = self.coordsPlayer2.copy()
      pTime = 0
      cTime = 0

      x1p1 = coordsPlayer1[0][0]
      y1p1 = coordsPlayer1[0][1]
      x2p1 = int(coordsPlayer1[0][0] + coordsPlayer1[2] * np.cos(coordsPlayer1[1]))
      y2p1 = int(coordsPlayer1[0][1] + coordsPlayer1[2] * np.sin(coordsPlayer1[1]))
      x1p2 = coordsPlayer2[0][0]
      y1p2 = coordsPlayer2[0][1]
      x2p2 = int(coordsPlayer2[0][0] + coordsPlayer2[2] * np.cos(coordsPlayer2[1]))
      y2p2 = int(coordsPlayer2[0][1] + coordsPlayer2[2] * np.sin(coordsPlayer2[1]))

      with self.mp_hands.Hands(
      model_complexity=0,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as hands:
        while self.cam.isOpened():
          if self.stopped:
            cv2.destroyAllWindows()
            self.cam.release()
            return

          success, image = self.cam.read()
          if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
          # mirror image
          image = cv2.flip(image, 1)

          self.imShape = image.shape
          # To improve performance, optionally mark the image as not writeable to
          # pass by reference.
          image.flags.writeable = False
          image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          results = hands.process(image)

          # Draw the hand annotations on the image.
          image.flags.writeable = True
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

          if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
              self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style())


              for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8:
                  if cx < w/2:
                    x1p1 = cx
                    y1p1 = cy
                  else:
                    x1p2 = cx
                    y1p2 = cy
                if id == 5:
                  if cx < w/2:
                    x2p1 = cx
                    y2p1 = cy
                  else:
                    x2p2 = cx
                    y2p2 = cy
            
            # Adjust P1 and P2 coords to fit in the field if the image shape is different than the field shape
            imageShape = image.shape
            if imageShape[1] != self.fieldShape[1] or imageShape[0] != self.fieldShape[0]:
              x1p1 = int(x1p1 * self.fieldShape[1] / self.imShape[1])
              y1p1 = int(y1p1 * self.fieldShape[0] / self.imShape[0])
              x2p1 = int(x2p1 * self.fieldShape[1] / self.imShape[1])
              y2p1 = int(y2p1 * self.fieldShape[0] / self.imShape[0])
              x1p2 = int(x1p2 * self.fieldShape[1] / self.imShape[1])
              y1p2 = int(y1p2 * self.fieldShape[0] / self.imShape[0])
              x2p2 = int(x2p2 * self.fieldShape[1] / self.imShape[1])
              y2p2 = int(y2p2 * self.fieldShape[0] / self.imShape[0])


            # Calculate P1 angle
            if x1p1 != x2p1:
              P1angle = np.arctan((y2p1 - y1p1) / (x2p1 - x1p1))
            else:
              P1angle = 0
            if x2p1 < x1p1:
              P1angle += np.pi
            coordsPlayer1 = [[x1p1, y1p1], P1angle, coordsPlayer1[2]]

            # Calculate P2 angle
            if x1p2 != x2p2:
              P2angle = np.arctan((y2p2 - y1p2) / (x2p2 - x1p2))
            else:
              P2angle = 0
            if x2p2 < x1p2:
              P2angle += np.pi
            coordsPlayer2 = [[x1p2, y1p2], P2angle+np.pi, coordsPlayer2[2]]

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            with self.camLock:
              self.coordsPlayer1 = coordsPlayer1
              self.coordsPlayer2 = coordsPlayer2
              self.image = image


  def stop(self):
    self.stopped = True

  def isStopped(self):
    return self.stopped

  def getCoords(self):
    with self.camLock:
      return self.coordsPlayer1, self.coordsPlayer2

  def getImage(self):
    with self.camLock:
      return self.image


if __name__ == "__main__":
  print("Camera handler for IndexFighter")
  print("Nothing to do here !")