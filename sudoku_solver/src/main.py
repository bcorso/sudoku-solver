'''
Created on Jan 5, 2013

@author: Brad
'''

import numpy
import timeit

print "=== SudokuSolver ==="
numpy.set_printoptions(linewidth=20)
setup = """\
from default_matrices import *
from solver import Solver
from answered_solver import AnsweredSolver
from singleton_solver import SingletonSolver
from naked_solver import NakedSolver
from hidden_solver import HiddenSolver
from pointing_solver import PointingSolver
from boxline_solver import BoxLineSolver
from xwing_solver import XWingSolver
from swordfish_solver import SwordFishSolver
from ywing_solver import YWingSolver
from simplecoloring_solver import SimpleColoringSolver
from xcycle_solver import XCycleSolver
from xychain_solver import XYChainSolver
from medusa3d_solver import Medusa3DSolver
from jellyfish_solver import JellyFishSolver
from sudoku_board import SudokuBoard, Cell, StrongChain, AlternatingChain,Node, Chain
from sudoku_solver_builder import SudokuSolverBuilder
m = SudokuBoard.str_to_matrix({0})
"""
#setups = (setup.format("","block_block1_str"),setup.format("","block_block2_str"),setup.format("","block_block3_str"),setup.format("","block_block4_str"),)
setups = (setup.format("jellyfish"),)
stmt = """\
solver = SudokuSolverBuilder(SudokuBoard(m),(AnsweredSolver(),
                                             SingletonSolver(),HiddenSolver(Solver.SINGLE),
                                             NakedSolver(Solver.DOUBLE),NakedSolver(Solver.TRIPLE),
                                             HiddenSolver(Solver.DOUBLE),HiddenSolver(Solver.TRIPLE),
                                             NakedSolver(Solver.QUAD),NakedSolver(Solver.QUINT),
                                             HiddenSolver(Solver.QUAD),HiddenSolver(Solver.QUINT),
                                             PointingSolver(Solver.DOUBLE),PointingSolver(Solver.TRIPLE),
                                             BoxLineSolver(Solver.DOUBLE),BoxLineSolver(Solver.TRIPLE),
                                             XWingSolver(),
                                             SimpleColoringSolver(),
                                             YWingSolver(),
                                             SwordFishSolver(),
                                             XCycleSolver(),
                                             XYChainSolver(),
                                             Medusa3DSolver(),
                                             JellyFishSolver(),
                                             )
                             )
#print solver.board.as_matrix()
#print solver.board.as_str()
solver.solve()
#print solver.board
print solver.board.as_matrix()
print ("Unsolved","Solved!")[solver.board.solved()]
print ("No Errors","Errors!")[solver.board.errors()]
"""
loops = 1
times = []
for i in range(len(setups)):
    print i
    times += [timeit.timeit(stmt=stmt, setup=setups[i], number=loops)/loops]
print times
print "total:",sum(times)
