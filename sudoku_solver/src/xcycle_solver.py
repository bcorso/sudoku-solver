'''
Created on Feb 2, 2013

@author: Brad
'''
from solver import Solver, SolvedSet, share_unit, visible_intersection
from sudoku_board import AlternatingChain

class XCycleSolver(Solver):
    NAME = "XCycle"
    
    def find(self, board, do_all = False):
        solved_sets = []
        for cell in board.as_list():
            chain_on = AlternatingChain(board, cell, 1, 10)
            solved_sets += self.find_rule1(board, chain_on)
            if solved_sets and not do_all:
                return solved_sets
            
        for cell in board.as_list():
            chain_off = AlternatingChain(board, cell, 0, 10)
            solved_sets += self.find_rule1(board, chain_off)
            if solved_sets and not do_all:
                return solved_sets
  
        for cell in board.as_list():
            chain_on = AlternatingChain(board, cell, 1, 10)
            solved_sets += self.find_rule2(board, chain_on)
            if solved_sets and not do_all:
                return solved_sets
            
        for cell in board.as_list():
            chain_off = AlternatingChain(board, cell, 0, 10)
            solved_sets += self.find_rule3(board, chain_off)
            if solved_sets and not do_all:
                return solved_sets
        return solved_sets
    
    def find_rule1(self, board, chain):
        '''Continuous Alternating Nice Loop - Weak link => off-chain candidates in same unit are OFF '''
        for value in chain.root.c:
            for leaf in chain.paths[value].get_leaves():
                if chain.paths[value].state == leaf.state and leaf.cell == chain.root:
                    solved_sets = []
                    for node in leaf.supernodes():
                        if node.parent != None and share_unit(node.cell,node.parent.cell):
                            removed = [cell for cell in visible_intersection(board,[node.cell,node.parent.cell]) if cell.check_remove(set([value]))]
                            if removed:
                                solved_sets += [SolvedSet(XCycleSolver(0, Solver.TYPE1), [node.cell, node.parent.cell], set([value]), removed)]
                    return solved_sets
        return []
    
    def find_rule2(self, board, chain):
        '''Discontinuous Alternating Nice Loop - candidate ON => candidate OFF (contradiction)'''
        for value in chain.root.c:
            for leaf in chain.paths[value].get_leaves():
                if chain.paths[value].state != leaf.state and leaf.cell == chain.root:
                    return [SolvedSet(XCycleSolver(0, Solver.TYPE2), [chain.root], set([value]), [chain.root])]
        return []
    
    def find_rule3(self, board, chain):
        '''Discontinuous Alternating Nice Loop - candidate ON => candidate OFF (contradiction)'''
        for value in chain.root.c:
            for leaf in chain.paths[value].get_leaves():
                if chain.paths[value].state != leaf.state and leaf.cell == chain.root:
                    return [SolvedSet(XCycleSolver(0, Solver.TYPE3), [chain.root], chain.root.c - set([value]), [chain.root])]
        return []