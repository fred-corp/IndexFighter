<h1 align="center">IndexFighter</h1>

<p align="center">
	<img width="200" height="200" margin-right="100%" src="https://github.com/fred-corp/IndexFighter/raw/main/images/icon/index%20fighter.png">
</p>

<p align="center">Like air hockey, but with your indexes !</p>
<p align="center">
<a href="https://github.com/fred-corp/IndexFighter/actions/workflows/codeql.yml"><img src="https://github.com/fred-corp/IndexFighter/actions/workflows/codeql.yml/badge.svg"></a>
<a href="https://github.com/fred-corp/IndexFighter/blob/main/LICENCE"><img src="https://img.shields.io/github/license/fred-corp/indexFighter"></a>
<a href="https://github.com/fred-corp/IndexFighter/issues"><img src="https://img.shields.io/github/issues/fred-corp/indexFighter"></a>
<a href="https://github.com/fred-corp/IndexFighter/commits/main"><img src="https://img.shields.io/github/last-commit/fred-corp/indexFighter"></a>
</p>

## Table of contents

- [Table of contents](#table-of-contents)
- [How to play](#how-to-play)
- [What is it ?](#what-is-it-)
- [Key challenges](#key-challenges)
- [Strategy](#strategy)
  - [Hand tracking](#hand-tracking)
  - [Multiplayer](#multiplayer)
  - [Real-time](#real-time)
  - [Dynamics](#dynamics)
- [Results](#results)
- [Further development ideas](#further-development-ideas)
- [Acknowledgements](#acknowledgements)

## How to play

> TODO: Develop details here

## What is it ?

IndexFighter is a game where two players use their indexes to control a paddle and hit a ball a bit like air hockey.  
Players can control paddle position and angle on their player side.

## Key challenges

- **Hand tracking** : the game must be playable with only hand tracking, no other input device
- **Multiplayer** : the game must be playable by two players on the same computer
- **Dynamics** : the game should handle realistic dynamics like friction, bounce angle, speed of attack, etc.
- **Real-time** : the game must be playable in real-time, with a low latency

## Strategy

### Hand tracking

The hand marker recognition is done with [mediapipe](https://pypi.org/project/mediapipe/), which is a python library containing a lot of machine learning models for computer vision. This simplifies the development of the game, as I didn't have to train my own models.

### Multiplayer

The game is played by two players controlling the position and angle of a paddle each. The game is played on a single computer with a single camera. Player A has the left side of the camera field to control their paddle, and player B has the right side of the camera field.

### Dynamics

The dynamics of the game, namely the bouncing of the puck on the borders and paddles, are handled by the `DynamicsHandler` class.  
This class calculates the new ball parameters (angle and speed) should a collision occur.

### Real-time

The game is written in python, and uses Threading to run the game logic and the hand tracking in parallel.

The `CameraHandler` class is responsible for the hand tracking. It runs a thread for the live hand tracking to decouple the tracking from the rest of the game code to make it run a bit smoother, and has getter functions for retrieving the player positions and angles.

The `DynamicsHandler` class is responsible for the game logic. It runs a thread for the game dynamics to render it independent of the hand tracking performance and thus be more precise, and has getter functions for retrieving the ball position and angle.

### Rendering

> TODO: Develop details here

## Results

> TODO: Develop details here

## Further development ideas

The project could be expanded by performing the following changes :

- Fix collision bugs : Sometimes, the puck collision with the paddles is not detected. This may be due to the fact that the collision detection is done with a simple distance calculation, and the puck can pass through the paddle without being detected.
- "Online multiplayer" : The players would be able to play on their own computer, provided they both have a camera and a computer. This would require a server to handle the game logic and hand tracking, and a client to display the game and send the hand tracking data to the server.
- Implement speed and friction : Like real air hockey, the puck should react to the speed of the paddles, and decelerate due to the friction of the playfield.
- Add a "power-up" system : The game could have power-ups that would affect the game dynamics, like a "speed boost" or a "slow down" power-up.

## Acknowledgements

Made with ❤️, lots of ☕️, and lack of 🛌  
Published under CreativeCommons BY-NC-SA 4.0

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
