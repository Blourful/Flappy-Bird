# Flipper Bird

A lightweight Flappy Bird-style arcade game built with Python and Pygame. Navigate the bird through gaps between pipes, avoid collisions, and try to achieve the highest score. The project includes custom sprites, sound effects, background music, and simple keyboard and mouse controls.

## Requirements

- Python 3
- Pygame

## Installation and Run

From the project root, install the dependency and start the game:

```bash
python -m pip install pygame
python game.py
```

Run the game from the project root because it loads image and audio files using relative paths under `assets/`.

## Controls

- Press `Space` or click the left mouse button to start the game.
- Press `Space` or click the left mouse button to make the bird flap.
- After hitting a pipe or the ground, press `Space` or click the play button to restart.
- Close the game window to exit.

## Project Structure

```text
.
├── game.py              # Main game logic
├── constants.py         # Game constants and resource loading
├── assets/
│   ├── audio/           # Sound effects and background music
│   └── sprites/         # Game image resources
└── flappybird/          # Original sprites and atlas documentation
```
