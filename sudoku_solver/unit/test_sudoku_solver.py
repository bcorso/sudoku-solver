'''
Created on Jan 5, 2013

@author: Brad
'''
from default_matrices import easy_matrix
from sudoku_board import SudokuBoard
from solver import Solver
import copy
import unittest

class SimpleSudokuSolverTestCase(unittest.TestCase):
    def setUp(self):
        self.solver = Solver(SudokuBoard(copy.deepcopy(easy_matrix)))

class GetPossibleTestCase(SimpleSudokuSolverTestCase):
    def runTest(self):
        self.assertEqual(self.solver.get_possible(0, 0), set([2,3,4]), 'incorrect possible set on element (0,0)')

class GetFirstUniqueTestCase(SimpleSudokuSolverTestCase):
    def runTest(self):
        unique = self.solver.get_first_unique()
        self.assertEqual(unique['i'], 3, 'incorrect first unique elelment i index')
        self.assertEqual(unique['j'], 8, 'incorrect first unique elelment j index')
        self.assertEqual(unique['value'], 9, 'incorrect first unique elelment value')

class NakedSingleSolverTestCase(SimpleSudokuSolverTestCase):
    def runTest(self):
        self.solver.naked_single_solver()
        self.assertEqual(self.solver.board.get_remaining(), 0, 'incorrect unsolved elements remaining')