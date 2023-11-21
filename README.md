# Sudoku Game

This Sudoku game is a Python-based puzzle game built with Pygame. It offers an interactive and graphical way to play Sudoku, with four levels of difficulty. There is also the ability to 'cheat' and solve the puzzles automatically.

## Installation

Before running the game, ensure you have Python installed on your system. If not, download and install Python from [python.org](https://www.python.org/). Additionally, this game requires Pygame, a set of Python modules designed for writing video games.

To install Pygame, run the following command in your terminal:

```bash
pip install pygame
```

## Running the Game
To start the game, navigate to the game's directory in your terminal and run the Python script:

```bash
sudoku.py
```

## Controls

- **Navigating the Board**: Use the mouse or arrow keys (↑↓←→) to select a cell on the Sudoku board.
- **Entering Numbers**: Click on a cell to select it, then type a number (1-9) to enter a temporary value in the cell. 
- **Confirming Numbers**: To confirm the entered number, re-enter the same number or press `Enter`. If the number is incorrect according to Sudoku rules, you will receive a strike. If it is correct, it will be accepted.
- **Solver**: Press the `Space` bar to activate the automatic Sudoku solver. It will visually display the process of solving the puzzle.
- **Reset board**: Press `R` to reset the board

## Strikes

The game tracks incorrect number placements. Each time you confirm an incorrect number, you'll receive a strike. Keep an eye on the number of strikes to gauge the difficulty you're having with the current puzzle.

## Enjoy the Game
