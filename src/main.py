import cv2
import sys
from CameraHandler import *
from PlayField import *
from DynamicsHandler import *

dynLock = Lock()



def startGame(debug=0):
  _debug = debug == 1
  borderX = 80
  borderY = 50
  friction = 1
  fieldShape = (720, 1280)
  #coordsPuck = [[640, 360], 20, 250, np.pi/4]
  coordsPuck = [[640, 360], 20, 100, 0]

  camHandler = CameraHandler(fieldShape)
  camHandler.start()
  playField = PlayField(fieldShape, borderX, borderY)

  coordsPlayer1, coordsPlayer2 = camHandler.getCoords()
  dynamicsHandler = DynamicsHandler(fieldShape, friction, borderX, borderY, coordsPlayer1, coordsPlayer2, coordsPuck)
  # Debug
  # dynamicsHandler.enableCollisions(player1=True, player2=False)
  dynamicsHandler.start()
  
  while True:
    coordsPlayer1, coordsPlayer2 = camHandler.getCoords()
    playfield = playField.getField(coordsPlayer1, coordsPlayer2, coordsPuck)
    dynamicsHandler.updatePlayerCoords(coordsPlayer1, coordsPlayer2)
    coordsPuck = dynamicsHandler.getPuckCoords()
    if _debug:
      cv2.imshow("Image", camHandler.getImage())
    cv2.imshow("Playfield", playfield)
    ##time.sleep(0.001)
    if cv2.waitKey(1) == 27:
      camHandler.stop()
      dynamicsHandler.stop()
      cv2.destroyAllWindows()
      break



if __name__ == '__main__':
  startGame(sys.argv[1] if len(sys.argv) > 1 else 0)
  print("Done")