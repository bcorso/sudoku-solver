'''
Created on Feb 4, 2013

@author: Brad
'''
from solver import Solver, visible_intersection, SolvedSet
from sudoku_board import XYChain

class XYChainSolver(Solver):
    NAME = "XY Chain"
    
    def find(self, board, do_all = False):
        solved_sets = []
        for cell in board.as_list():
            xychain = XYChain(board, cell,10)
            solved_sets += self.find_rule1(board, xychain)
            if solved_sets and not do_all:
                return solved_sets
        return solved_sets
    
    def find_rule1(self, board, chain):
        ''' '''
        for value in chain.root.c:
            for leaf in chain.paths[value].get_leaves(value):
                if leaf.value == value and leaf.state == 1 and leaf.cell != chain.root:
                    removed = [cell for cell in visible_intersection(board, [leaf.cell, chain.root]) if cell.check_remove(set([value]))]
                    if removed:
                        return [SolvedSet(XYChainSolver(0, Solver.TYPE1), [leaf.cell, chain.root], set([value]), removed)]
        return []