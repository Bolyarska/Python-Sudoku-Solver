import unittest
import errno
import sys
from Sudoku_solver_2 import SudokuSolver

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


class TestSudokuSolver(unittest.TestCase):
    def test_solve(self):
        solver = SudokuSolver(matrix)
        solver.solve()
        # Check that all rows, columns, and 3x3 boxes contain no duplicate numbers
        for i in range(9):
            self.assertEqual(len(set(solver.matrix[i])), 9)  # check row
            self.assertEqual(len(set(solver.matrix[j][i] for j in range(9))), 9)  # check column
            row_start = (i // 3) * 3
            col_start = (i % 3) * 3
            self.assertEqual(len(set(
                solver.matrix[j][k] for j in range(row_start, row_start + 3) for k in range(col_start, col_start + 3))),
                             9)  # check 3x3 box


if __name__ == '__main__':
    unittest.main()
