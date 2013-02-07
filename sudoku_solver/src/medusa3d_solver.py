'''
Created on Feb 5, 2013

@author: Brad
'''
from solver import Solver, share_unit, SolvedSet, visible_intersection
from sudoku_board import Strong3DChain

class Medusa3DSolver(Solver):
    NAME = "3D Medusa"
    
    def find(self, board, do_all = False):
        solved_sets = []
        rules = [self.find_rule1, self.find_rule2, self.find_rule3, self.find_rule4, self.find_rule5, self.find_rule6]
        for rule in rules:
            for cell in board.as_list():
                chain = Strong3DChain(board, cell,1,10)
                solved_sets += rule(board, chain)
                if solved_sets and not do_all:
                    return solved_sets
        return solved_sets

    def find_rule1(self, board, chain):
        ''' twice in a cell '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.cell == node2.cell and node1.value != node2.value and node1.state == node2.state:
                        solved_sets = []
                        for node in set(chain.paths[v].subnodes(state = node1.state)):
                            solved_sets += [SolvedSet(Medusa3DSolver(0, Solver.TYPE1), [node1.cell], set([node.value]), [node.cell])]
                        return solved_sets
        return []
    
    def find_rule2(self, board, chain):
        ''' twice in a unit '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.cell != node2.cell and node1.value == node2.value and node1.state == node2.state and share_unit(node1.cell,node2.cell):
                        solved_sets = []
                        for node in set(chain.paths[v].subnodes(state = node1.state)):
                            solved_sets += [SolvedSet(Medusa3DSolver(0, Solver.TYPE2), [node1.cell, node2.cell], set([node.value]), [node.cell])]
                        return solved_sets
        return []
    
    def find_rule3(self, board, chain):
        ''' twice in a cell '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.cell == node2.cell and node1.state != node2.state and len(node1.cell.c - set([node1.value,node2.value])) > 0:
                        return [SolvedSet(Medusa3DSolver(0, Solver.TYPE3), [node1.cell], node1.cell.c - set([node1.value,node2.value]), [node1.cell])]
        return []
    
    def find_rule4(self, board, chain):
        ''' twice in a unit '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.cell != node2.cell and node1.value == node2.value and node1.state != node2.state and share_unit(node1.cell,node2.cell):
                        removed = [cell for cell in visible_intersection(board, [node1.cell,node2.cell]) if cell.check_remove(set([node1.value]))]
                        if removed:
                            return [SolvedSet(Medusa3DSolver(0, Solver.TYPE4), [node1.cell, node2.cell], set([node1.value]) ,removed)]
        return []
    
    def find_rule5(self, board, chain):
        ''' twice in a unit '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                for j,node2 in enumerate(possible):
                    if j > i and node1.cell != node2.cell and node1.value == node2.value and node1.state != node2.state:
                        removed = [cell for cell in visible_intersection(board, [node1.cell,node2.cell]) if cell.check_remove(set([node1.value]))]
                        if removed:
                            return [SolvedSet(Medusa3DSolver(0, Solver.TYPE5), [node1.cell, node2.cell], set([node1.value]) ,removed)]
        return []
    
    def find_rule6(self, board, chain):
        ''' same color in a unit opposite color in cell '''
        for v in chain.root.c:
            possible = chain.paths[v].subnodes()
            for i,node1 in enumerate(possible):
                solved_sets = []
                for j,node2 in enumerate(possible):
                    if j > i and node1.cell != node2.cell and node1.value != node2.value and node1.state != node2.state and share_unit(node1.cell,node2.cell):
                        if node1.value in node2.cell.c:
                            solved_sets += [SolvedSet(Medusa3DSolver(0, Solver.TYPE6), [node1.cell, node2.cell], set([node1.value]), [node2.cell])]
                        if node2.value in node1.cell.c:
                            solved_sets += [SolvedSet(Medusa3DSolver(0, Solver.TYPE6), [node1.cell, node2.cell], set([node2.value]), [node1.cell])]
                return solved_sets
        return []