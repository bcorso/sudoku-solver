'''
Created on Jan 5, 2013

@author: Brad
'''

from default_matrices import easy_matrix
from sudoku_board import SudokuBoard
import unittest

class SimpleSudokuBoardTestCase(unittest.TestCase):
    def setUp(self):
        self.board = SudokuBoard(easy_matrix)

class GetSizeTestCase(SimpleSudokuBoardTestCase):
    def runTest(self):
        self.assertEqual(self.board.N, 9, 'incorrect default size')
        self.assertEqual(self.board.n, 3, 'incorrect default n (box size)')
        
class GetTestCase(SimpleSudokuBoardTestCase):
    def runTest(self):
        self.assertEqual(self.board.get(0,0), 0, 'incorrect element gotten at (0,0)')
        self.assertEqual(self.board.get(3,4), 2, 'incorrect element gotten at (3,4)')
        self.assertEqual(self.board.get(6,6), 8, 'incorrect element gotten at (6,6)')

class SetTestCase(SimpleSudokuBoardTestCase):
    def runTest(self):
        self.board.set(0,0,5)
        self.board.set(3,4,3)
        self.board.set(6,6,6)
        self.assertEqual(self.board.get(0,0), 5, 'incorrect element set at (0,0)')
        self.assertEqual(self.board.get(3,4), 3, 'incorrect element set at (3,4)')
        self.assertEqual(self.board.get(6,6), 6, 'incorrect element set at (6,6)')

class GetRowTestCase(SimpleSudokuBoardTestCase):
    def runTest(self):
        self.assertEqual(self.board.get_row(0), [0,0,0, 1,0,5, 0,6,8], 'incorrect first (0) row')
        self.assertEqual(self.board.get_row(4), [5,0,0, 0,0,0, 0,0,3], 'incorrect middle (4) row')
        self.assertEqual(self.board.get_row(8), [7,9,0, 4,0,1, 0,0,0], 'incorrect last (8) row')
        
class GetColTestCase(SimpleSudokuBoardTestCase):
    def runTest(self):
        self.assertEqual(self.board.get_col(0), [0,0,9, 0,5,0, 0,1,7], 'incorrect first (0) col')
        self.assertEqual(self.board.get_col(4), [0,0,0, 2,0,7, 0,0,0], 'incorrect middle (4) col')
        self.assertEqual(self.board.get_col(8), [8,1,0, 0,3,0, 5,0,0], 'incorrect last (8) col')

class GetBoxTestCase(SimpleSudokuBoardTestCase):
    def runTest(self):
        self.assertEqual(self.board.get_box(1,1), [0,0,0, 0,0,0, 9,0,1], 'incorrect first (1,1) box')
        self.assertEqual(self.board.get_box(4,4), [0,2,6, 0,0,0, 8,7,0], 'incorrect middle (4,4) box')
        self.assertEqual(self.board.get_box(7,7), [8,0,5, 0,0,0, 0,0,0], 'incorrect last (7,7) box')

class GetRemainingTestCase(SimpleSudokuBoardTestCase):
    def runTest(self):
        self.assertEqual(self.board.get_remaining(), 55, 'incorrect remaining unsolved elements')
        
