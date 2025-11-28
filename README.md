# Tile Block Puzzle Game 🧱
A playable web link (once deployed): https://FaisalAhmed21.github.io/Tile-Block-Puzzle-Game/

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

## How to Run

1. Download the Tile-Block-Puzzle-Game.py raw file to your local machine
2. Open the Tile-Block-Puzzle-Game.py file in vs code and run the code 

Hosting on the web (one-click playable link)
-----------------------------------------

This project is a Pygame application. To provide a clickable web link that opens the game in a browser, we can package it to WebAssembly/HTML using "pygbag" and deploy the build to GitHub Pages. I've added a GitHub Actions workflow that will automatically build and publish the web version when you push this repository to GitHub.

Quick steps to publish:

1. Create a repository on GitHub and push this project (all files) to the `main` (or `master`) branch.
2. The GitHub Action (`.github/workflows/deploy-gh-pages.yml`) will run automatically. It:
  - installs dependencies from `requirements.txt`
  - installs `pygbag`
  - runs `pygbag --release --target web -o build .`
  - deploys the generated `build/web` folder to the `gh-pages` branch
3. After the workflow completes, your site will be available at: `https://<your-github-username>.github.io/<your-repo-name>/` (GitHub Pages URL). Use that link to open the game on any device.

If you prefer to build and test locally before pushing:

PowerShell (local build):
```powershell
# create and activate a virtual environment (recommended)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pygbag
# build web + test locally (output in ./build/web)
python -m pygbag --release --target web -o build .
```

You can open `build/web/index.html` in a browser (or serve the folder with a simple HTTP server) to test the page locally before pushing.

Notes and caveats
- pygbag wraps pygame for the browser using WebAssembly and supports many (but not all) pygame APIs; the game may need small runtime adjustments. If the Action build fails, open the Action log to see missing modules or runtime exceptions and I can help patch minimal incompatibilities.
- If you want me to create the GitHub repository, set up topics, or help edit code to increase browser compatibility, tell me and I can prepare patches.

## Controls

- **Left Arrow**: Move block left
- **Right Arrow**: Move block right
- **Down Arrow**: Move block down faster
- **Up Arrow**: Rotate block
- **UI Buttons**:
  - Red X: Close game
  - Green Button: Pause/Resume game
  - Blue Button: Restart game

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

