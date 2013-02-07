'''
Created on Jan 19, 2013

@author: Brad
'''
from solver import Solver, has_size, visible_intersection, SolvedSet

class YWingSolver(Solver):
    NAME = "YWing"
    
    def find(self, board, do_all = False):
        solved_sets = []
        possible = has_size(board.as_list(),2,2)
        ywings = [(pivot,cell1,cell2) for i,cell1 in enumerate(possible) for j,cell2 in enumerate(possible) for pivot in visible_intersection(board, [cell1,cell2]) if j > i and pivot.c == cell1.c ^ cell2.c and len(cell1.c & cell2.c) == 1 ]
        for pivot, cell1, cell2 in ywings:
            remove = [cell for cell in visible_intersection(board, [cell1,cell2]) if cell != pivot and cell.check_remove(cell1.c & cell2.c)]
            if remove:
                solved_sets += [SolvedSet(self, [pivot, cell1, cell2], cell1.c & cell2.c, remove)]
                if not do_all:
                        return solved_sets
        return solved_sets
   
        
        