'''
Created on Feb 7, 2013

@author: Brad
'''
from naked_solver import NakedSolver
from solver import Solver

class UniqueRectangleSolver(Solver):
    NAME = "Unique Rectangle"
    TYPES = {1:"Rule1",2:"Rule2",3:"Rule3",4:"Rule4"}
    
    def find(self, board, do_all = False):
        solved_sets = []
        rules = [self.find_rule1]
        for rule in rules:
            solved_sets += rule(board, do_all)
            if solved_sets and not do_all:
                return solved_sets
        return solved_sets

    def find_rule1(self, board, do_all = False):
        naked_solver = NakedSolver(Solver.DOUBLE)
        for i in range(board.N):
            possible = naked_solver.find_in_list(board.get_row(i))
            if len(possible) == 2:
        
                
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.state == node2.state and node1.cell != node2.cell and share_unit(node1.cell,node2.cell):
                        return [SolvedSet(SimpleColoringSolver(0, Solver.TYPE2), [node1.cell, node2.cell], set([v]), [cell for cell in set(chain.paths[v].subcells(v,node1.state))])]
        return []