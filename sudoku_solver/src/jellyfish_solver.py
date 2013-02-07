'''
Created on Feb 5, 2013

@author: Brad
'''
from solver import Solver, has_count, has_size, SolvedSet

class JellyFishSolver(Solver):
    NAME = "JellyFish"
    TYPES = {1:"Row",2:"Col"}
    
    def find(self, board, do_all = False):
        solved_sets = []
        possible = [has_count(has_size(board.get_row(i),2,None), 2, 4) for i in range(board.N) ]
        jellyfish = [(k1,v1+v2+v3+v4) for i,p1 in enumerate(possible) for j,p2 in enumerate(possible) for k,p3 in enumerate(possible) for l,p4 in enumerate(possible) \
                      for k1,v1 in p1.items() for k2,v2 in p2.items() for k3,v3 in p3.items() for k4,v4 in p4.items() if p1 and p2 and p3 and p4 and l > k > j > i \
                      and k1 == k2 == k3 == k4 and len(set([c1.j for c1 in v1] + [c2.j for c2 in v2] + [c3.j for c3 in v3] + [c4.j for c4 in v4])) == 4]
        for candidate, jellyfish_cells in jellyfish:
            removed = []
            for col in set([cell.j for cell in jellyfish_cells]):
                removed += [cell for cell in board.get_col(col) if cell not in jellyfish_cells and cell.check_remove(set([candidate]))]
            if removed:
                solved_sets += [SolvedSet(JellyFishSolver(0,1), jellyfish_cells, set([candidate]), removed)]
                if not do_all:
                    return solved_sets      

        possible = [has_count(has_size(board.get_col(i),2,None), 2, 4) for i in range(board.N) ]
        jellyfish = [(k1,v1+v2+v3+v4) for i,p1 in enumerate(possible) for j,p2 in enumerate(possible) for k,p3 in enumerate(possible) for l,p4 in enumerate(possible) \
                      for k1,v1 in p1.items() for k2,v2 in p2.items() for k3,v3 in p3.items() for k4,v4 in p4.items() if p1 and p2 and p3 and p4 and l > k > j > i \
                      and k1 == k2 == k3 == k4 and len(set([c1.i for c1 in v1] + [c2.i for c2 in v2] + [c3.i for c3 in v3] + [c4.i for c4 in v4])) == 4]
        for candidate, jellyfish_cells in jellyfish:
            removed = []
            for row in set([cell.i for cell in jellyfish_cells]):
                removed = [cell for cell in board.get_row(row) if cell not in jellyfish_cells and cell.check_remove(set([candidate]))]
            if removed:
                solved_sets += [SolvedSet(JellyFishSolver(0,2), jellyfish_cells, set([candidate]), removed)]
                if not do_all:
                    return solved_sets
        return solved_sets