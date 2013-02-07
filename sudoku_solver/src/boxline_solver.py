'''
Created on Jan 13, 2013

@author: Brad
'''
from solver import Solver, has_size, has_count, SolvedSet

class BoxLineSolver(Solver):
    NAME = "Box-Line"
    TYPES = {1:'Row', 2:'Col'} 
    
    def find(self, board, do_all = False):
        solved_sets = []
        for i in range(board.N):
            possible = has_size(board.get_row(i), 2, None)
            for candidate, cells in has_count(possible, self.level, self.level).items():
                if all([cell.k == cells[0].k for cell in cells]):
                    removed_cells = [cell for cell in board.get_box(cells[0].k) if not cell.answer and cell not in cells and cell.check_remove(set([candidate]))]
                    if removed_cells:
                        solved_sets += [SolvedSet(BoxLineSolver(self.level,1), cells, set([candidate]), removed_cells)]
                        if not do_all:
                            return solved_sets
                        
            possible = has_size(board.get_col(i), 2, None)
            for candidate, cells in has_count(possible, self.level,self.level).items():
                if all([cell.k == cells[0].k for cell in cells]):
                    removed_cells = [cell for cell in board.get_box(cells[0].k) if not cell.answer and cell not in cells and cell.check_remove(set([candidate]))]
                    if removed_cells:
                        solved_sets += [SolvedSet(BoxLineSolver(self.level,2), cells, set([candidate]), removed_cells)]
                        if not do_all:
                            return solved_sets
        return solved_sets