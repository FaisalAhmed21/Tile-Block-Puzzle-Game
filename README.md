# Tile Block Puzzle Game 🧱

A Python-based puzzle game that combines elements of classic block-falling games with unique obstacle mechanics, built using Pygame.

## Features

- Dynamic block-falling gameplay with various shapes
- Color-coded blocks and obstacles
- Real-time scoring system
- Lives system with obstacle collision penalties
- Timer-based gameplay (60 seconds per round)
- Interactive control buttons:
  - Pause/Play functionality
  - Restart game option
  - Close game button
- Grid-based movement system
- Block rotation mechanics
- Row clearing system with bonus points
- Obstacle generation system
- Game over screen with multiple end conditions
- Visual effects including:
  - Grid lines
  - Block shading
  - Color gradients
  - Hover effects on buttons

## Prerequisites

- Python 3.7 or higher
- Pygame library

## Installation

1. Ensure Python is installed on your system. You can check your Python version with:
```bash
python3 --version
```
2. Install Pygame using pip:
```bash
pip install pygame
```

## Gameplay Rules

1. **Objective**: Score as many points as possible within the 60-second time limit
2. **Scoring**:
   - 10 points for successfully placing a block
   - Additional 10 points for clearing a row
   - Bonus 20 points for clearing multiple rows simultaneously
3. **Lives System**:
   - Start with 3 lives
   - Lose a life when colliding with obstacles
   - Game ends when all lives are lost
4. **Game Over Conditions**:
   - Running out of lives
   - Time expiration (60 seconds)
   - Block collision at spawn point


## Game Components

- Main game grid
- Falling blocks system
- Obstacle generation
- Score tracking
- Timer system
- Lives counter
- Control buttons
- Game over screen
- Visual feedback system

## Development

Built using:
- Python3
- Pygame for graphics and game loop
- Object-oriented design for UI components
- Collision detection system
- Color manipulation for visual effects

