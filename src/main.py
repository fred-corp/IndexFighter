import cv2
import sys
from CameraHandler import *
from PlayField import *
from DynamicsHandler import *
from Player import *

dynLock = Lock()



def startGame(debug=0):
  _debug = int(debug) == 1
  borderX = 80
  borderY = 50
  friction = 1
  goalHeight = 300
  fieldShape = (720, 1280)
  coordsPuck = [[640, 360], 20, 0, np.pi/4]
  startDelay = 5

  camHandler = CameraHandler(fieldShape)
  camHandler.start()
  playField = PlayField(fieldShape, borderX, borderY, goalHeight)
  player1 = Player()
  player2 = Player()

  coordsPlayer1, coordsPlayer2 = camHandler.getCoords()
  player1.setParams(coordsPlayer1)
  player2.setParams(coordsPlayer2)
  dynamicsHandler = DynamicsHandler(fieldShape, friction, borderX, borderY, goalHeight, player1, player2, coordsPuck)
  # Debug
  # dynamicsHandler.enableCollisions(player1=True, player2=False)
  dynamicsHandler.start()
  time0 = time.time()
  started = False
  while True:
    # wait 10 seconds before releasing the puck
    if time.time() - time0 > startDelay and started == False:
      dynamicsHandler.setPuckCoords([[640, 360], 20, 250, np.pi/4])
      started = True
    coordsPlayer1, coordsPlayer2 = camHandler.getCoords()
    player1.setParams(coordsPlayer1)
    player2.setParams(coordsPlayer2)
    playfield = playField.getField(player1, player2, coordsPuck)
    dynamicsHandler.updatePlayerCoords(player1, player2)
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
    if cv2.waitKey(1) & 0xFF == ord('r'):
      player1.score = 0
      player2.score = 0
      started = False
      time0 = time.time()
      dynamicsHandler.setPuckCoords([[640, 360], 20, 0, np.pi/4])



if __name__ == '__main__':
  startGame(debug = sys.argv[1] if len(sys.argv) > 1 else 0)
  print("Done")