'''
Created on Feb 7, 2013

@author: Brad
'''
from naked_solver import NakedSolver
from solver import Solver, SolvedSet, visible_intersection, has_size, has_count, \
    candidate_count
from sudoku_board import Cell

class UniqueRectangleSolver(Solver):
    NAME = "Unique Rectangle"
    
    def find(self, board, do_all = False):
        solved_sets = []
        rules = [self.find_rule1, self.find_rule2, self.find_rule3, self.find_rule4]
        for rule in rules:
            solved_sets += rule(board, do_all)
            if solved_sets and not do_all:
                return solved_sets
        return solved_sets
    
    def find_rule1(self, board, do_all = False):                        
        naked_solver = NakedSolver(Solver.DOUBLE)
        for row in range(board.N):
            for floor in naked_solver.find_in_list(board.get_row(row)):
                for i, f1 in enumerate(floor):
                    for j, f2 in enumerate(floor):
                        ceil1 = [cell for cell in board.get_col(f1.j) if i != j and cell != f1 and len(set([f1.k, f2.k, cell.k])) == 2 and cell.c == f1.c]
                        ceil2 = [board.get(cell.i, f2.j) for cell in ceil1 if board.get(cell.i, f2.j).check_remove(f1.c)]
                        if ceil1 and ceil2:
                            return [SolvedSet(UniqueRectangleSolver(0, Solver.TYPE1), list(floor) + ceil1 + ceil2, f1.c, ceil2)]
        return []
    
    def find_rule2(self, board, do_all = False):
        naked_solver = NakedSolver(Solver.DOUBLE)
        for row in range(board.N):
            for floor in naked_solver.find_in_list(board.get_row(row)):
                for i, f1 in enumerate(floor):
                    for j, f2 in enumerate(floor):
                        ceils1 = [cell for cell in board.get_col(f1.j) if i != j and cell != f1 and len(set([f1.k, f2.k, cell.k])) == 2 and cell.c.issuperset(f1.c) and not f1.c.issuperset(cell.c)]
                        for ceil1 in ceils1:
                            cell = board.get(ceil1.i, f2.j)
                            ceil2 = cell if cell.c.issuperset(ceil1.c) and ceil1.c.issuperset(cell.c) else None                        
                            if ceil2:
                                remove = [cell for cell in visible_intersection(board,[ceil1,ceil2]) if cell.check_remove(ceil1.c & ceil2.c - f1.c) ]
                                if remove:
                                    return [SolvedSet(UniqueRectangleSolver(0, Solver.TYPE2), [f1,f2,ceil1,ceil2], ceil1.c & ceil2.c - f1.c, remove)]
        for col in range(board.N):
            for floor in naked_solver.find_in_list(board.get_col(col)):
                for i, f1 in enumerate(floor):
                    for j, f2 in enumerate(floor):
                        ceils1 = [cell for cell in board.get_row(f1.i) if i != j and cell != f1 and len(set([f1.k, f2.k, cell.k])) == 2 and cell.c.issuperset(f1.c) and not f1.c.issuperset(cell.c)]
                        for ceil1 in ceils1:
                            cell = board.get(f2.i, ceil1.j)
                            ceil2 = cell if cell.c.issuperset(ceil1.c) and ceil1.c.issuperset(cell.c) else None                        
                            if ceil2:
                                print ceil2.c
                                print ceil1.c
                                remove = [cell for cell in visible_intersection(board,[ceil1,ceil2]) if cell.check_remove(ceil1.c & ceil2.c - f1.c) ]
                                if remove:
                                    return [SolvedSet(UniqueRectangleSolver(0, Solver.TYPE2), [f1,f2,ceil1,ceil2], ceil1.c & ceil2.c - f1.c, remove)]
        return []
                                
    def find_rule3(self, board, do_all = False):
        naked_solver = NakedSolver(Solver.DOUBLE)
        for row in range(board.N):
            for floor in naked_solver.find_in_list(board.get_row(row)):
                for i, f1 in enumerate(floor):
                    for j, f2 in enumerate(floor):
                        ceils1 = [cell for cell in board.get_col(f1.j) if i != j and cell != f1 and len(set([f1.k, f2.k, cell.k])) == 2 and cell.c.issuperset(f1.c) and len(cell.c - f1.c) == 1]
                        for ceil1 in ceils1:
                            cell = board.get(ceil1.i, f2.j)
                            ceil2 = cell if cell.c.issuperset(f1.c) and len(cell.c - f1.c) == 1 and not cell.c.issuperset(ceil1.c) else None                        
                            if ceil2:
                                pair = [cell for cell in visible_intersection(board,[ceil1,ceil2]) if cell != f1 and cell != f2 and cell.c == ceil1.c ^ ceil2.c ]
                                if pair:
                                    remove = [cell for cell in visible_intersection(board,[ceil1,ceil2,pair[0]]) if cell != f1 and cell != f2 and cell.check_remove(pair[0].c)]
                                    if remove:
                                        return [SolvedSet(UniqueRectangleSolver(0, Solver.TYPE3), [f1,f2,ceil1,ceil2,pair[0]], pair[0].c, remove)]
        for col in range(board.N):
            for floor in naked_solver.find_in_list(board.get_col(col)):
                for i, f1 in enumerate(floor):
                    for j, f2 in enumerate(floor):
                        ceils1 = [cell for cell in board.get_row(f1.i) if i != j and cell != f1 and len(set([f1.k, f2.k, cell.k])) == 2 and cell.c.issuperset(f1.c) and len(cell.c - f1.c) == 1]
                        for ceil1 in ceils1:
                            cell = board.get(f2.i, ceil1.j)
                            ceil2 = cell if cell.c.issuperset(f1.c) and len(cell.c - f1.c) == 1 and not cell.c.issuperset(ceil1.c) else None                       
                            if ceil2:
                                pair = [cell for cell in visible_intersection(board,[ceil1,ceil2]) if cell != f1 and cell != f2 and cell.c == ceil1.c ^ ceil2.c ]
                                if pair:
                                    remove = [cell for cell in visible_intersection(board,[ceil1,ceil2,pair[0]]) if cell != f1 and cell != f2 and cell.check_remove(pair[0].c)]
                                    if remove:
                                        return [SolvedSet(UniqueRectangleSolver(0, Solver.TYPE3), [f1,f2,ceil1,ceil2,pair[0]], pair[0].c, remove)]
        return []
    
    def find_rule4(self, board, do_all = False):
        naked_solver = NakedSolver(Solver.DOUBLE)
        for row in range(board.N):
            for floor in naked_solver.find_in_list(board.get_row(row)):
                for i, f1 in enumerate(floor):
                    for j, f2 in enumerate(floor):
                        ceils1 = [cell for cell in board.get_col(f1.j) if i != j and cell != f1 and len(set([f1.k, f2.k, cell.k])) == 2 and cell.c.issuperset(f1.c) and not f1.c.issuperset(cell.c)]
                        for ceil1 in ceils1:
                            ceil2 = board.get(ceil1.i, f2.j)
                            for x in f1.c:
                                if ceil2.c.issuperset(f1.c) and len(ceil2.c - f1.c) > 0 and (candidate_count(board.get_row(ceil2.i),x) == 2 or candidate_count(board.get_box(ceil2.k),x) == 2):                  
                                    return [SolvedSet(UniqueRectangleSolver(0, Solver.TYPE4), [f1,f2,ceil1,ceil2], f1.c - set([x]), [ceil1,ceil2])]
        for col in range(board.N):
            for floor in naked_solver.find_in_list(board.get_col(col)):
                for i, f1 in enumerate(floor):
                    for j, f2 in enumerate(floor):
                        ceils1 = [cell for cell in board.get_row(f1.i) if i != j and cell != f1 and len(set([f1.k, f2.k, cell.k])) == 2 and cell.c.issuperset(f1.c) and not f1.c.issuperset(cell.c)]
                        for ceil1 in ceils1:
                            ceil2 = board.get(f2.i, ceil1.j)
                            for x in f1.c:
                                if ceil2.c.issuperset(f1.c) and len(ceil2.c - f1.c) > 0 and (candidate_count(board.get_col(ceil2.j),x) == 2 or candidate_count(board.get_box(ceil2.k),x) == 2):                  
                                    return [SolvedSet(UniqueRectangleSolver(0, Solver.TYPE4), [f1,f2,ceil1,ceil2], f1.c - set([x]), [ceil1,ceil2])]
        return []