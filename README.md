# IndexFighter

Like air hockey, but with your indexes !

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
- **Real-time** : the game must be playable in real-time, with a low latency
- **Dynamics** : the game should handle realistic dynamics like friction, bounce angle, speed of attack, etc.

## Strategy

### Hand tracking

The hand tracking is done with [mediapipe](https://pypi.org/project/mediapipe/), which is a python library containing a lot of machine learning models for computer vision. This simplifies the development of the game, as I didn't have to train my own models.
 
### Multiplayer

> TODO: Develop details here

### Real-time

> TODO: Develop details here

The game is written in python, and uses Threading to run the game logic and the hand tracking in parallel.

### Dynamics

> TODO: Develop details here

## Results

> TODO: Develop details here

## Further development ideas

> TODO: Develop details here

## Acknowledgements

Made with ❤️, lots of ☕️, and lack of 🛌  
Published under CreativeCommons BY-NC-SA 4.0

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)  
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
