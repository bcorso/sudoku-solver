'''
Created on Jan 13, 2013

@author: Brad
'''
from solver import Solver, has_count, has_size, SolvedSet

class XWingSolver(Solver):
    NAME = "XWing"
    TYPES = {1:"Row",2:"Col"}
    
    def find(self, board, do_all = False):
        solved_sets = []
        possible = [has_count(has_size(board.get_row(i),2,None), 2, 2) for i in range(board.N) ]
        xwings = [(k1,v1+v2) for i,p1 in enumerate(possible) for j,p2 in enumerate(possible) for k1,v1 in p1.items() for k2,v2 in p2.items() if p1 and p2 and j > i and k1 == k2 and len(set([c1.j for c1 in v1])|set([c2.j for c2 in v2])) == 2]
        for candidate, xwing_cells in xwings:
            for col in set([cell.j for cell in xwing_cells]):
                removed = [cell for cell in board.get_col(col) if cell not in xwing_cells and cell.check_remove(set([candidate]))]
                if removed:
                    solved_sets += [SolvedSet(XWingSolver(0,1), xwing_cells, set([candidate]), removed)]
                    if not do_all:
                        return solved_sets
                    
        possible = [has_count(has_size(board.get_col(j),2,None), 2, 2) for j in range(board.N) ]
        xwings = [(k1,v1+v2) for i,p1 in enumerate(possible) for j,p2 in enumerate(possible) for k1,v1 in p1.items() for k2,v2 in p2.items() if p1 and p2 and j > i and k1 == k2 and all([c2.j in set([c1.j for c1 in v1]) for c2 in v2])]
        for candidate, xwing_cells in xwings:
            for row in set([cell.i for cell in xwing_cells]):
                removed = [cell for cell in board.get_row(row) if cell not in xwing_cells and cell.check_remove(set([candidate]))]
                if removed:
                    solved_sets += [SolvedSet(XWingSolver(0,2), xwing_cells, set([candidate]), removed)]
                    if not do_all:
                        return solved_sets
        return solved_sets