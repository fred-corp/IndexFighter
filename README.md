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
- [Demo](#demo)
- [How to run](#how-to-run)
- [What is it ?](#what-is-it-)
- [Key challenges](#key-challenges)
- [Strategy](#strategy)
  - [Hand tracking](#hand-tracking)
  - [Multiplayer](#multiplayer)
  - [Dynamics](#dynamics)
  - [Real-time](#real-time)
  - [Rendering](#rendering)
- [Results](#results)
- [Further development ideas](#further-development-ideas)
- [Acknowledgements](#acknowledgements)

## Demo

<p  align="center"><img width="200" height="200" src="images/Demo.gif"></p>

> A 500x500 video is available [here](images/Demo.mov)

## How to run

You need to have a working installation of Python 3.10, and the pip package manager.

Then, you'll need to install the required libraries with pip :

```sh
pip install -r requirements.txt
```

(Oh and of course you'll need a webcam, the resolution should not matter but an aspect ratio of 16:9 is better)

Finally, you can download or clone the repo, and launch the game with the following command at the root of the repo :

```sh
python src/main.py
```

> You may need to specify the python version :
>
> ```sh
> python3.10 src/main.py
> ```

You can add a debug argument to show the webcam image by adding a `1` at the end of the command :

```sh
python src/main.py 1
```

You can reset the game by pressing the `r` key, and you can exit the game by pressing the `esc` key.

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

The `Playfield` class is used to create the image of the playfield with the player data, puck data, etc.  
It does not have its own thread so the playfield is asked to be generated rendered in the `main.py` script.

## Results

The code works, yay !  
There are some issues where some collisions with the paddles are not detected, or stray collisions that seem to happen randomly anywhere the playfield. This could be fixed by refactoring and optimizing the code.

## Further development ideas

The project could be expanded by performing the following changes :

- Fix collision bugs : Sometimes, the puck collision with the paddles is not detected. This may be due to the fact that the collision detection is done with a simple distance calculation, and the puck can pass through the paddle without being detected.
- "Online multiplayer" : The players would be able to play on their own computer, provided they both have a camera and a computer. This would require a server to handle the game logic and hand tracking, and a client to display the game and send the hand tracking data to the server.
- Implement speed and friction : Like real air hockey, the puck should react to the speed of the paddles, and decelerate due to the friction of the playfield.
- Add a "power-up" system : The game could have power-ups that would affect the game dynamics, like a "speed boost" or a "slow down" power-up.
- Add a "score" system : The game could have a score system, and the first player to reach a certain score would win the game (now the gale runs indefinitely).

## Acknowledgements

Made with ❤️, lots of ☕️, and lack of 🛌  
Published under CreativeCommons BY-NC-SA 4.0

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
