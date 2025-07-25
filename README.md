# sudoku it

A Python implementation of a Sudoku solver using backtracking algorithm.

## How it works

The program creates a 9x9 Sudoku grid, places one random number as a seed, then uses backtracking to solve the complete puzzle following standard Sudoku rules:
- Each row must contain digits 1-9 without repetition
- Each column must contain digits 1-9 without repetition  
- Each 3x3 box must contain digits 1-9 without repetition

## Usage

```bash
python main.py
```

The program will display the initial grid with the random seed, then show the solved puzzle.