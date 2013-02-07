'''
Created on Jan 13, 2013

@author: Brad
'''
from solver import Solver, cell_union, SolvedSet, has_size

class NakedSolver(Solver):
    NAME = "Naked"
    
    def find(self, board, do_all = False):
        solved_sets = []
        func_list = [board.get_row, board.get_col, board.get_box]
        for func in func_list:
            for i in range(board.N):
                for possible in self.find_in_list(func(i)):
                    cells_removed = [cell for cell in func(i) if cell not in possible and not cell.answer and cell.check_remove(cell_union(possible))] 
                    if cells_removed:
                        solved_sets += [SolvedSet(self, possible, cell_union(possible), cells_removed)]
                        if not do_all:
                            return solved_sets
        return solved_sets
    
    def find_in_list(self, cell_list):
        possible = has_size(cell_list, 2, self.level)
        found = []
        if len(possible) >= self.level:
            if self.level == 2:
                found = [(a,b) for i,a in enumerate(possible) for j,b in enumerate(possible) if j > i and len(a.c|b.c) == 2]
            if self.level == 3:
                found = [(a,b,c) for i,a in enumerate(possible) for j,b in enumerate(possible) for k,c in enumerate(possible) if k > j > i and len(a.c|b.c|c.c) == 3]
            if self.level == 4:
                found = [(a,b,c,d) for i,a in enumerate(possible) for j,b in enumerate(possible) for k,c in enumerate(possible) for l,d in enumerate(possible) if l > k > j > i and len(a.c|b.c|c.c|d.c) == 4]
            if self.level == 5:
                found = [(a,b,c,d,e) for i,a in enumerate(possible) for j,b in enumerate(possible) for k,c in enumerate(possible) for l,d in enumerate(possible) for m,e in enumerate(possible) if m > l > k > j > i and len(a.c|b.c|c.c|d.c|e.c) == 5]
        return found