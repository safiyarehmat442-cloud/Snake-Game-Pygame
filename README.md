# Simple Snake Game

This project is a simple Snake Game developed using Python and Pygame.

## Description

The game is inspired by the classic Snake Game that was popular on keypad phones. The player controls a snake that can move in different directions across the screen.

The snake dies if it collides with:
- The game boundaries (walls)
- Its own body
- Obstacles present in the game

Each time the snake eats a food particle:
- The score increases
- The snake's body grows longer

## Features

- Snake movement in four directions
- Food collection and score tracking
- Snake growth after eating food
- Obstacle collision detection
- High score tracking
- Sound effects for:
  - Starting the game
  - Eating food
  - Game over
- Simple and interactive user interface

## Technologies Used

- Python
- Pygame
- NumPy

## How to Run

1. Install the required libraries:

```bash
pip install pygame numpy
```

2. Run the game:

```bash
python Snake-Game.py
```