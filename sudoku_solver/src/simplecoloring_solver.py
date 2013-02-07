'''
Created on Jan 18, 2013

@author: Brad
'''
from solver import Solver, share_unit, SolvedSet, visible_intersection
from sudoku_board import StrongChain

class SimpleColoringSolver(Solver):
    NAME = "Simple Coloring"
    
    def find(self, board, do_all = False):
        solved_sets = []
        rules = [self.find_rule2,self.find_rule4,self.find_rule5]
        for rule in rules:
            done = []
            for cell in board.as_list():
                if cell not in done:
                    chain = StrongChain(board, cell,1,5)
                    solved_sets += rule(board, chain)
                    if solved_sets and not do_all:
                        return solved_sets
                    for value in chain.root.c:
                        done += chain.paths[value].subcells()
        return solved_sets

    def find_rule2(self, board, chain):
        ''' same color twice in a unit '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.state == node2.state and node1.cell != node2.cell and share_unit(node1.cell,node2.cell):
                        return [SolvedSet(SimpleColoringSolver(0, Solver.TYPE2), [node1.cell, node2.cell], set([v]), [cell for cell in set(chain.paths[v].subcells(v,node1.state))])]
        return []
    
    def find_rule4(self, board, chain):
        ''' two colors in a unit '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.state != node2.state and node1.cell != node2.cell and share_unit(node1.cell,node2.cell):
                        removed = [cell for cell in visible_intersection(board, [node1.cell,node2.cell]) if cell.check_remove(set([v]))]
                        if removed:
                            return [SolvedSet(SimpleColoringSolver(0, Solver.TYPE4), [node1.cell, node2.cell], set([v]), removed)]
        return []
                        
    def find_rule5(self, board, chain):
        ''' two colors elsewhere '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.state != node2.state and node1.cell != node2.cell:
                        removed = [cell for cell in visible_intersection(board, [node1.cell,node2.cell]) if cell.check_remove(set([v]))]
                        if removed:
                            return [SolvedSet(SimpleColoringSolver(0, Solver.TYPE5), [node1.cell, node2.cell], set([v]), removed)]
        return []