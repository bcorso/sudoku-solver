'''
Created on Jan 13, 2013

@author: Brad
'''
from solver import Solver, SolvedSet

class SingletonSolver(Solver):
    NAME = "Singleton"
    
    def solve(self, board, do_all = False):
        solved_sets = self.find(board, do_all = do_all)
        for solved_set in solved_sets:
            board.remove_from_cells(solved_set.solved_cells, solved_set.removed)
            singleton = solved_set.solver_cells[0] 
            singleton.solve(list(singleton.c)[0])
        return solved_sets
    
    def find(self, board, do_all = False):
        solved_sets = [SolvedSet(self,[cell], cell.c, [cell]) for cell in board.as_list() if not cell.answer and len(cell.c) == 1]
        if not do_all:
            if solved_sets:
                return [solved_sets[0]]
            return []
        return solved_sets