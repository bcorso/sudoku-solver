'''
Created on Jan 13, 2013

@author: Brad
'''
from solver import Solver, has_size, has_count, SolvedSet

class PointingSolver(Solver):
    NAME = "Pointing"
    TYPES = {1:'Row',2:'Col'}
    
    def find(self, board, do_all = False):
        solved_sets = []
        for i in range(board.N):
            possible = has_size(board.get_box(i), 2, None)
            for candidate, cells in has_count(possible, self.level,self.level).items():
                if all([cell.i == cells[0].i for cell in cells]):
                    removed_cells = [cell for cell in board.get_row(cells[0].i) if not cell.answer and cell not in cells and cell.check_remove(set([candidate]))]
                    if removed_cells:
                        solved_sets += [SolvedSet(PointingSolver(self.level,1), cells, set([candidate]), removed_cells)]
                        if not do_all:
                            return solved_sets
                        
                if all([cell.j == cells[0].j for cell in cells]):
                    removed_cells = [cell for cell in board.get_col(cells[0].j) if not cell.answer and cell not in cells and cell.check_remove(set([candidate]))]
                    if removed_cells:
                        solved_sets += [SolvedSet(PointingSolver(self.level,2), cells, set([candidate]), removed_cells)]
                        if not do_all:
                            return solved_sets
        
        return solved_sets