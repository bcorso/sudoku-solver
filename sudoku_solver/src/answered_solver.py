'''
Created on Jan 13, 2013

@author: Brad
'''
from solver import Solver, SolvedSet

class AnsweredSolver(Solver):
    NAME = "Answered"
    
    def __init__(self):
        super(AnsweredSolver,self).__init__()
        self.answered_cells = []
        
    def solve(self, board, do_all = False):
        solved_sets = self.find(board, do_all = do_all)
        for solved_set in solved_sets:
            board.remove_from_cells(solved_set.solved_cells, solved_set.removed)
            self.answered_cells += [solved_set.solver_cells[0]]
        return solved_sets
    
    def find(self, board, do_all = False):
        solved_sets = []
        for cell in [cell for cell in board.as_list() if cell not in self.answered_cells and cell.answer]:
            solved_cells = [check_cell for check_cell in board.get_row(cell.i).tolist()+board.get_col(cell.j).tolist()+board.get_box(cell.k).tolist() if not check_cell.answer and check_cell.check_remove(set([cell.answer]))]
            if solved_cells:
                solved_sets += [SolvedSet(AnsweredSolver(), [cell], set([cell.answer]), solved_cells)]
                if not do_all:
                    return solved_sets
        return solved_sets