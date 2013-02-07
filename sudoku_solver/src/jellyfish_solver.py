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
        possible = [has_count(has_size(board.get_row(i),2,None), 2, 3) for i in range(board.N) ]
        swordfish = [(k1,v1+v2+v3) for i,p1 in enumerate(possible) for j,p2 in enumerate(possible) for k,p3 in enumerate(possible) for k1,v1 in p1.items() for k2,v2 in p2.items() for k3,v3 in p3.items() if p1 and p2 and p3 and k > j > i and k1 == k2 == k3 and len(set([c1.j for c1 in v1])|set([c2.j for c2 in v2])|set([c3.j for c3 in v3])) == 3]
        for candidate, swordfish_cells in swordfish:
            for col in set([cell.j for cell in swordfish_cells]):
                removed = [cell for cell in board.get_col(col) if cell not in swordfish_cells and cell.check_remove(set([candidate]))]
                if removed:
                    solved_sets += [SolvedSet(JellyFishSolver(0,1), swordfish_cells, set([candidate]), removed)]
                    if not do_all:
                        return solved_sets

        possible = [has_count(has_size(board.get_col(j),2,None), 2, 3) for j in range(board.N) ]
        swordfish = [(k1,v1+v2+v3) for i,p1 in enumerate(possible) for j,p2 in enumerate(possible) for k,p3 in enumerate(possible) for k1,v1 in p1.items() for k2,v2 in p2.items() for k3,v3 in p3.items() if p1 and p2 and p3 and k > j > i and k1 == k2 == k3 and len(set([c1.i for c1 in v1])|set([c2.i for c2 in v2])|set([c3.i for c3 in v3])) == 3]
        for candidate, swordfish_cells in swordfish:
            for row in set([cell.i for cell in swordfish_cells]):
                removed = [cell for cell in board.get_row(row) if cell not in swordfish_cells and cell.check_remove(set([candidate]))]
                if removed:
                    solved_sets += [SolvedSet(JellyFishSolver(0,2), swordfish_cells, set([candidate]), removed)]
                    if not do_all:
                        return solved_sets
        return solved_sets