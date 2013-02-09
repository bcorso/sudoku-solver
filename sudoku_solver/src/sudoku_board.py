'''
Created on Jan 6, 2013

@author: Brad
'''
from collections import Counter
from solver import strong_links, weak_links, visible_intersection
import copy
import math
import numpy

                        
class Chain(object):
    def __init__(self, board, cell, root_state = 1, level = None):
        self.links = []
        self.root = cell
        self.state = root_state
        self.level = level
        self.paths = {}      
        for value in self.root.c:
            self.paths[value] = Node(cell, value, root_state)
    
    def full_extend(self, board, path):
        size = 0
        while(path.size() > size and (self.level == None or path.length() < self.level)):
            size = path.size()
            self.extend(board, path)
    
    def length(self):
        return max([0]+[self.paths[value].length() for value in self.root.c])
    
    def extend(self, board, node, value, root_value):
        return 0
    
    def remove_dangling_leaves(self):
        for value in self.root.c:
            counts = Counter([node.cell for node in self.paths[value].subnodes()])
            while(1 in counts.keys()):
                for leaf in self.paths[value].get_leaves(value):
                    if counts[leaf.cell] == 1:
                        leaf.parent.remove_child(leaf)
                counts = Counter([node.cell for node in self.paths[value].subnodes()])
    
    def remove_noncycles(self):
        for value in self.root.c:
            while(True):
                remove = [leaf for leaf in self.paths[value].get_leaves(value) if leaf.cell != self.root]
                if remove:
                    for leaf in remove:
                        leaf.parent.remove_child(leaf)
                else:
                    break
    
    def __str__(self):
        return '{0}'.format(''.join([str(self.paths[value]) for value in self.root.c]))

    def __repr__(self):
        return 'Chain(links={0},root={1},state={2},level={3},paths={4})'.format(self.links, self.root,self.state,self.level,self.paths)

class StrongChain(Chain):
    def __init__(self, board, cell, root_state = 1, level = None):
        super(StrongChain,self).__init__(board, cell, root_state, level)
        for path in self.paths.values():
            self.full_extend(board, path)
        
    def extend(self, board, root):
        for leaf in root.get_leaves():
            if not (leaf.parent != None and leaf.cell == self.root):
                links = strong_links(board,leaf.cell,2,leaf.value)
                for cell in links:
                    if not (leaf.parent != None and leaf.parent.cell == cell):
                        child = Node(cell, leaf.value, (1,0)[leaf.state == 1])
                        leaf.add_child(child)

class AlternatingChain(Chain):
    def __init__(self, board, cell, root_state = 1, level = None):
        super(AlternatingChain,self).__init__(board, cell, root_state, level)
        for path in self.paths.values():
            self.full_extend(board, path)
        self.remove_noncycles()
        #self.remove_dangling_leaves()
        
    def extend(self, board, root):
        for leaf in root.get_leaves():
            if not (leaf.parent != None and leaf.cell == self.root):
                links = []
                if leaf.state == 0:
                    links += strong_links(board,leaf.cell,2,leaf.value)
                if leaf.state == 1:
                    links += weak_links(board,leaf.cell,leaf.value)
                links = list(set(links))
                for cell in links:
                    if not (leaf.parent != None and leaf.parent.cell == cell):
                        child = Node(cell, leaf.value, (1,0)[leaf.state == 1])
                        leaf.add_child(child)

class XYChain(Chain):
    def __init__(self, board, cell, level = None):
        super(XYChain,self).__init__(board, cell, 0, level)
        for path in self.paths.values():
            self.full_extend(board, path)
        #self.remove_noncycles()
    
    def extend(self, board, root):
        for leaf in root.get_leaves():
            if len(leaf.cell.c) == 2 and not (leaf.value == root.value and leaf.state == 1 and len(visible_intersection(board,[leaf.cell,self.root])) > 0):
                if not (leaf.parent != None and leaf.cell == root.cell and leaf.value == root.value):
                    if (leaf.parent == None or leaf.parent.cell != leaf.cell):
                        bivalue = (leaf.cell.c - set([leaf.value])).pop()
                        child = Node(leaf.cell, bivalue, (1,0)[leaf.state == 1])
                        leaf.add_child(child)
                    else:
                        links = []
                        if leaf.state == 0:
                            links += strong_links(board, leaf.cell, 2, leaf.value)
                        if leaf.state == 1:
                            links += weak_links(board, leaf.cell, leaf.value)
                        links = list(set([cell for cell in links if len(cell.c) == 2]))
                        links = [cell for cell in links if root.value in cell.c]+[cell for cell in links if root.value not in cell.c]
                        for cell in links:
                            if not (leaf.parent != None and leaf.parent.cell == cell):
                                child = Node(cell, leaf.value, (1,0)[leaf.state == 1])
                                leaf.add_child(child)

class Strong3DChain(Chain):
    def __init__(self, board, cell, root_state = 1, level = None):
        super(Strong3DChain,self).__init__(board, cell, root_state, level)
        self.pair = []
        for path in self.paths.values():
            self.full_extend(board, path)
            self.pair += [(path.cell,path.value)]
            
    def extend(self, board, root):
        for leaf in root.get_leaves():
            if not (leaf.cell == root.cell and leaf.value == root.value and leaf.parent != None):
                if len(leaf.cell.c) == 2 and (leaf.parent == None or leaf.parent.cell != leaf.cell):
                    bivalue = (leaf.cell.c - set([leaf.value])).pop()
                    child = Node(leaf.cell, bivalue, (1,0)[leaf.state == 1])
                    leaf.add_child(child)
                    self.pair += [(child.cell,child.value)]
                for cell in strong_links(board, leaf.cell, 2, leaf.value):
                    if (cell, leaf.value) not in self.pair:
                        child = Node(cell, leaf.value, (1,0)[leaf.state == 1])
                        leaf.add_child(child)
                        self.pair += [(child.cell,child.value)]

class Node:
    def __init__(self, cell, value, state):
        self.parent = None
        self.cell = cell
        self.value = value
        self.state = state
        self.children = []
    
    def add_child(self, node):
        self.children += [node]
        node.parent = self
    
    def remove_child(self,child):
        self.children.remove(child)
    
    def length(self):
        if not self.children:
            return 0
        return max([1+child.length() for child in self.children])
    
    def size(self):
        return (0,1)[self.parent == None] + len(self.children) + sum([child.size() for child in self.children])
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def get_leaves(self, value = None):
        if not self.children:
            return ([],[self])[value == None or value == self.value]
        return [leaf for child in self.children for leaf in child.get_leaves(value)]
    
    def supernodes(self):
        if self.parent == None:
            return [self]
        return [self] + self.parent.supernodes()
    
    def subnodes(self, value = None, state = None):
        return ([],[self])[(value == None or value == self.value) and (state == None or state == self.state)] + [node for child in self.children for node in child.subnodes(value,state)]
    
    def subcells(self, value = None, state = None):
        return [node.cell for node in self.subnodes(value, state)]
    
    def level(self):
        if self.parent == None:
            return 0
        else:
            return self.parent.level() + 1
    
    def __str__(self):
        return "{0}{1} {2}:{3}{4}".format('\n'+''.join(['\t']*self.level()),self.cell,self.value, ("OFF","On")[self.state == 1], (' -->', ' ==>')[self.state == 1] + ''.join([str(node) for node in self.children]) if len(self.children) > 0 else '')
    
    def __repr__(self):
        return '{0}Node(cell={1},value= {2},states={3},children={4})'.format('\n'+''.join(['\t']*self.level()),self.cell, self.value, self.state, self.children)

class Cell:
    def __init__(self, i, j, board_size, candidates, answer = 0):
        self.i = i
        self.j = j
        self.board_size = board_size
        self.box_size = int(math.sqrt(board_size))
        self.k = self.get_box()
        self.answer = answer
        self.c = candidates
        if self.answer:
            self.c = set([])
    
    def indices(self):
        return (self.i, self.j)
    
    def get_row(self):
        return self.i
    
    def get_col(self):
        return self.j
    
    def get_box(self):
        return self.i//self.box_size*self.box_size + self.j//self.box_size
    
    def remove(self, candidates):
        removing = self.check_remove(candidates)
        if removing:
            self.c -= removing
        return removing
    
    def check_remove(self, candidates):
        if self.c and candidates:
            removing = self.c & candidates
            remaining = self.c - candidates
            return (set([]), removing)[len(removing) > 0 and len(remaining) > 0]
    
    def solve(self, answer):
        self.answer = answer
        self.c = set([])
    
    def __str__(self):
        return '({0},{1})'.format(self.i+1,self.j+1,(self.c,self.answer)[self.answer>0])
        #return 'Cell({0},{1} = {2})'.format(self.i+1,self.j+1,(list(self.c),self.answer)[self.answer>0])
    
    def __repr__(self):
        return 'Cell(index=({0},{1}),candidates={2})'.format(self.i+1,self.j+1,(self.c,self.answer)[self.answer>0])

class SudokuBoard:
    
    def __init__(self, M):
        self.M = copy.deepcopy(M)
        self.N = int(len(M)) 
        self.n = int(math.sqrt(len(M)))
        self.Cells = numpy.array([[ Cell(i, j, self.N, set(range(1,self.N+1)), answer = M[i][j]) for j in range(self.N)] for i in range(self.N)])
    
    @classmethod
    def str_to_matrix(cls, str_):
        N = int(math.sqrt(len(str_)))
        n = int(math.sqrt(N))
        m = []
        for i in range(N):
            temp = []
            for j in range(N):
                if str_[i*N+j] != ".":
                    temp += [int(str_[i*N+j])]
                else:
                    temp += [0]
            m += [temp]
        return numpy.array(m)
    
    def as_str(self):
        return ''.join([str(('.',self.Cells[i,j].answer)[self.Cells[i,j].answer > 0]) for i in range(self.N) for j in range(self.N)])
    
    def as_matrix(self):
        return numpy.array([[self.Cells[i,j].answer for j in range(self.N)] for i in range(self.N)])                        
    
    def as_list(self):
        return self.Cells.reshape(self.N*self.N)
    
    def get(self,i,j):
        return self.Cells[i, j]
    
    def set(self,i,j,value):
        self.Cells[i, j][1] = value
        
    def get_row(self,i):
        '''returns row i of the sudoku matrix as a 1xN matrix'''
        return (numpy.array(self.Cells[i,:]).tolist(), [])[i == None]
    
    def get_col(self,j):
        '''returns column j of the sudoku matrix as a 1xN matrix'''
        return (numpy.array(self.Cells[:,j]).tolist(), [])[j == None]
    
    def get_box(self,k):
        '''returns box that contains element i,j of the sudoku matrix as a nxn matrix'''
        i, j = k//self.n*self.n, k%self.n*self.n
        return (numpy.array(self.Cells[i:i+self.n, j:j+self.n].reshape(self.N)).tolist(), [])[k == None]
    
    def remove_from_row(self, i, candidates, exceptions = []):
        return [cell for cell in self.get_row(i) if cell not in exceptions and cell.remove(candidates)]
    
    def remove_from_col(self, j, candidates, exceptions = []):
        return[cell for cell in self.get_col(j) if cell not in exceptions and cell.remove(candidates)]
            
    def remove_from_box(self, k, candidates, exceptions = []):
        return [cell for cell in self.get_box(k) if cell not in exceptions and cell.remove(candidates)]
    
    def remove_from_cells(self, cells, candidates):
        for cell in cells:
            cell.remove(candidates)
    
    def get_answered(self, exceptions = []):
        return [cell for cell in self.as_list() if cell.answer and cell not in exceptions]
    
    def errors(self):
        for i in range(self.N):
            row = [cell.answer for cell in self.get_row(i) if cell.answer]
            if len(set(row)) != len(row):
                print "row", i
                return True
            col = [cell.answer for cell in self.get_row(i) if cell.answer]
            if len(set(col)) != len(col):
                print "col", i
                return True
            box = [cell.answer for cell in self.get_row(i) if cell.answer]
            if len(set(box)) != len(box):
                print "box", i
                return True
        return False
    
    def solved(self):
        for cell in self.as_list():
            if not cell.answer:
                return False
        return True
    
    def __str__(self):
        return str(self.Cells)
    
    def __repr__(self):
        return self.__str__()