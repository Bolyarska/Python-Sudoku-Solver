"""the code provides a single solution for a 9x9 sudoku puzzle. If the starting puzzle is invalid there won't be a solution.

The data is derived from the 'input' file and the solution and time taken to produce it is presented in the 'Result' file.

expected format for the matrix (example):

0 2 0 0 0 0 0 6 3
0 0 0 0 0 5 4 0 1
0 0 3 0 0 9 0 8 0
0 0 0 2 0 0 0 0 0
0 0 7 4 0 0 8 0 0
0 0 1 0 7 0 0 0 0
0 0 0 0 3 0 0 0 0
9 0 0 0 0 0 0 0 0
7 0 5 0 0 0 0 0 0
"""

import time
import errno
import sys

start_time = time.time()

matrix = []

try:
    with open('input', 'r') as file:
        for line in file:
            row = line.strip('\n').split()
            can_be_number = [n.isnumeric() for n in row]
            if len(row) == 9 and all(can_be_number):
                matrix.append([int(n) for n in row])
            else:
                print('Invalid input file format')
                sys.exit(1)
except IOError as x:
    if x.errno == errno.ENOENT:
        print("input file doesn't exist.")
    elif x.errno == errno.EACCES:
        print("input file cannot be read.")
    else:
        print("Error reading input file.")
    sys.exit(1)


class SudokuSolver:
    def __init__(self, matrix):
        self.matrix = matrix

    def find_empty_cell(self, start_row, start_col):
        """Finds the first empty cell in the matrix starting from the last checked empty cell.
         Returns the coordinates of the cell or None if no empty cell exists"""
        for row in range(start_row, 9):
            for col in range(start_col, 9):
                if self.matrix[row][col] == 0:
                    return row, col
            start_col = 0
        return None

    def get_possible_values(self, row, col):
        """Given the coordinates of an empty cell (row, col), determines the set of possible values that could be placed in that cell
        Returns a set of possible values for that cell"""
        possible_values = set(range(1, 10))

        # Remove values in the same row, column, and box
        for i in range(9):
            possible_values.discard(self.matrix[row][i])
            possible_values.discard(self.matrix[i][col])

        # Check the values in the same 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                possible_values.discard(self.matrix[i][j])

        return possible_values

    def solve(self, start_row=0, start_col=0):
        empty_cell = self.find_empty_cell(start_row, start_col)
        if not empty_cell:
            return True

        row, col = empty_cell
        possible_values = self.get_possible_values(row, col)

        if not possible_values:
            return False

        for value in possible_values:
            self.matrix[row][col] = value

            if self.solve(row, col + 1):  # Recursion
                return True

            self.matrix[row][col] = 0  # Backtracks the last cell if no solution is found with the current value

        return False

    def display_board(self):  # Displays the solved matrix
        result = ''
        for row in range(9):
            if row % 3 == 0 and row != 0:
                result += "- " * 11 + '\n'

            for i in range(9):
                if i % 3 == 0 and i != 0:
                    result += "|" + ' '

                if i == 8:
                    result += str(self.matrix[row][i]) + '\n'
                else:
                    result += str(self.matrix[row][i]) + ' '

        return result


solver = SudokuSolver(matrix)

try:
    with open('Result', 'w') as result:
        if solver.solve():
            result.write('Solved Board:\n')
            solution = solver.display_board()
            result.write(solution)
        else:
            print("Board cannot be solved.")
except IOError as x:
    if x.errno == errno.EACCES:
        print("Solution file cannot be accessed.")
    sys.exit(1)

print(f'Time taken: {time.time() - start_time}')
