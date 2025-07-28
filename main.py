from random import randint

class Sudoku:
    """
    A Sudoku is a 9x9 grid where each row, column, and 3x3 box must contain the digits 1-9 without repetition.
    The grid is represented as a list of lists, where each inner list represents a row.
    """
    def __init__(self):
        self.grid: list[list[int]] = [[0] * 9 for _ in range(9)]
        self.length: int = 9
        self.width: int = 9

    def set_random_seed(self):
        """
        Set a random seed for the Sudoku grid.
        This method fills the grid with random values between 1 and 9 in a single cell.
        """
        self.grid[randint(0, 8)][randint(0, 8)] = randint(1, 9)

    def return_seed_position(self) -> tuple[int, int]:
        """
        Return the position of the randomly set seed in the Sudoku grid.
        """
        positions = [(i, j) for i in range(self.length) for j in range(self.width) if self.grid[i][j] != 0]
        return positions[0] if positions else (-1, -1)
    
    def set_random_grid(self, quantity: int):
        """
        Set a random grid with a specified number of filled cells.
        :param quantity: Number of cells to fill with random values (1-81).
        """
        if not (1 <= quantity <= 81):
            raise ValueError("Quantity must be between 1 and 81.")
        
        for _ in range(quantity):
            row, col = randint(0, 8), randint(0, 8)
            value = randint(1, 9)
            while not self.verify_cell_value(row, col, value):
                row, col = randint(0, 8), randint(0, 8)
                value = randint(1, 9)
            self.grid[row][col] = value

    def print_grid(self):
        """
        Print the Sudoku grid in a readable format.
        Empty cells are represented by 0.
        """
        for i, row in enumerate(self.grid):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            formatted_row = []
            for j, num in enumerate(row):
                if j % 3 == 0 and j != 0:
                    formatted_row.append("|")
                formatted_row.append(str(num) if num != 0 else '.')
            print(" ".join(formatted_row))
        print()

    def list_possibles_values_in_cell(self, row: int, col: int) -> list[int]:
        """
        List all possible values that can be placed in the specified cell according to Sudoku rules.
        """
        if self.grid[row][col] != 0:
            return []

        possible_values = set(range(1, 10))

        # Check row
        possible_values -= set(self.grid[row])

        # Check column
        possible_values -= {self.grid[r][col] for r in range(self.length)}

        # Check 3x3 box
        box_row_start: int = (row // 3) * 3
        box_col_start: int = (col // 3) * 3
        possible_values -= {self.grid[r][c] for r in range(box_row_start, box_row_start + 3)
                            for c in range(box_col_start, box_col_start + 3)}

        return list(possible_values)

    def verify_cell_value(self, row: int, col: int, value: int) -> bool:
        """
        Verify if placing a value in the specified cell is valid according to Sudoku rules.
        :param row: Row index (0-8)
        :param col: Column index (0-8)
        :param value: Value to place in the cell (1-9)
        :return: True if valid, False otherwise
        """
        if not (1 <= value <= 9):
            return False
        
        # Check row
        if value in self.grid[row]:
            return False
        
        # Check column
        for r in range(self.length):
            if self.grid[r][col] == value:
                return False
        
        # Check 3x3 box
        box_row_start: int = (row // 3) * 3
        box_col_start: int = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if self.grid[r][c] == value:
                    return False
        
        return True

    def solve_grid_backtracking(self, col: int, row: int) -> bool:
        """
        Solve the Sudoku grid using the Backtracking algorithm.
        It fills the grid recursively, trying each number from 1 to 9 in each empty cell.
        It moves to the cell immediately to the right, and wraps to the beginning of the next row when reaching the end of a row.
        """
        # If we've reached past the last row, the puzzle is solved
        if row == self.length:
            return True

        # Move to the next cell
        next_col = (col + 1) % self.width # Move to the next column, wrap around if needed
        next_row = row + 1 if next_col == 0 else row # Continue to the next row if we wrapped around

        # If the current cell is already filled, skip to the next cell
        if self.grid[row][col] != 0:
            return self.solve_grid_backtracking(next_col, next_row)

        # Try placing each value from 1 to 9 in the current cell
        for value in range(1, 10):
            if self.verify_cell_value(row, col, value):
                self.grid[row][col] = value
                if self.solve_grid_backtracking(next_col, next_row):
                    return True
                self.grid[row][col] = 0  # Backtrack if placing value didn't lead to a solution
        return False
    
    def validate_full_grid(self) -> bool:
        """
        Validate the entire Sudoku grid to ensure it follows Sudoku rules.
        This checks all rows, columns, and 3x3 boxes for duplicates.
        """
        # Check if the grid is completely filled
        for i in range(self.length):
            # Check if each row has unique numbers (ignoring zeros)
            if len(set(self.grid[i])) != len([num for num in self.grid[i] if num != 0]):
                return False
            
            # Check if each column has unique numbers (ignoring zeros)
            col = [self.grid[j][i] for j in range(self.length)]
            if len(set(col)) != len([num for num in col if num != 0]):
                return False
            
            # Check each 3x3 box for unique numbers (ignoring zeros)
            box_row_start = (i // 3) * 3
            box_col_start = (i % 3) * 3
            box = [self.grid[r][c] for r in range(box_row_start, box_row_start + 3)
                   for c in range(box_col_start, box_col_start + 3)]
            if len(set(box)) != len([num for num in box if num != 0]):
                return False
        
        return True

class SudokuTreeNode:
    """
    A node in a tree representing a Sudoku cell.
    Each node contains the position of the cell (x_pos, y_pos) and a list of possible values that can be placed in that cell (keys).
    The node can have multiple children, representing the next cell to be filled in the Sudoku grid, with each child node containing the possible values for that cell based on the current value of the key in its parent node.
    """
    def __init__(self, x_pos: int, y_pos: int, possible_values: list[int], is_root: bool = False):
        self.x_pos: int = x_pos
        self.y_pos: int = y_pos
        self.is_root: bool = is_root
        self.possible_values: list[int] = possible_values
        self.children: list[SudokuTreeNode] = []

class SudokuTree:
    def __init__(self):
        self.sudoku: Sudoku = Sudoku().set_random_seed() # Initialize Sudoku with a random seed
        seed_pos = self.sudoku.return_seed_position()
        self.root: SudokuTreeNode = SudokuTreeNode(
            x_pos=seed_pos[0], 
            y_pos=seed_pos[1],
            possible_values=self.sudoku.list_possibles_values_in_cell(seed_pos[0], seed_pos[1]),
            is_root=True
        )
        

def main():
    sudoku = Sudoku()
    # sudoku.set_random_seed()  # Set a random seed in the Sudoku grid
    sudoku.set_random_grid(10)  # Fill the grid with 10 random values
    sudoku.print_grid()
    if sudoku.solve_grid_backtracking(0, 0):
        print("Sudoku solved successfully:")
        sudoku.print_grid()
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()