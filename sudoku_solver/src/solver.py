'''
Created on Jan 4, 2013

@author: Brad

'''
class SolvedSet():
    def __init__(self, solver, solver_cells, removed, solved_cells):
        self.solver = solver
        self.solver_cells = solver_cells
        self.removed = removed
        self.solved_cells = solved_cells
    
    def __str__(self):
        return "{0}: {1}, removed {2} from {3} Cells:{4}".format(self.solver, \
             '['+','.join([str(cell) for cell in self.solver_cells])+']', \
             '['+','.join([str(cell) for cell in list(self.removed)])+']', \
             len(self.solved_cells) , \
             '['+','.join([str(cell) for cell in self.solved_cells])+']')
    def __repr__(self):
        return "SolvedSet(solver={0}, solver_cells={1}, removed={2}, solved_cells={3})".format( self.solver_name, self.solver_cells, self.removed, self.solved_cells)

class Solver(object):
    NAME = "Solver"
    ALL,SINGLE, DOUBLE, TRIPLE, QUAD, QUINT = range(0,6)
    LEVELS = {0:'',1:'Single',2:'Double',3:'Triple',4:'Quad',5:'Quint'}
    TYPE1,TYPE2,TYPE3,TYPE4,TYPE5,TYPE6 = range(1,7)
    TYPES = {0:'',1:'Rule1',2:'Rule2',3:'Rule3',4:'Rule4',5:'Rule5',6:'Rule6'}
    
    def __init__(self, solver_level = ALL, solver_type = ALL):
        super(Solver, self).__init__()
        self.type = solver_type
        self.level = solver_level
        
    def solve(self, board, do_all = False):
        solved_sets = self.find(board, do_all = do_all)
        for solved_set in solved_sets:
            board.remove_from_cells(solved_set.solved_cells, solved_set.removed)
        return solved_sets
    
    def __str__(self):
        return "{0}{1}{2}".format(self.NAME, (""," " +self.LEVELS[self.level])[self.level > 0], (""," - " +self.TYPES[self.type])[self.type > 0])
    def __repr__(self):
        return self.__str__()

def cell_union(cell_list, exceptions = []):
    return set.union(*[cell.c for cell in cell_list if cell not in exceptions])

def cell_intersection(cell_list, exceptions = []):
    return set.intersection(*[cell.c for cell in cell_list if cell not in exceptions])

def cell_difference(set_, cell_list, exceptions = []):
    return set_.difference(*[cell.c for cell in cell_list if cell not in exceptions])

def has_size(cell_list, min_, max_):
    return [cell for cell in cell_list if not cell.answer and (len(cell.c) >= min_, True)[min_ == None] and (len(cell.c) <= max_, True)[max_ == None]]

def has_count(cell_list, min_, max_):
    return {candidate:cells for candidate,cells in count(cell_list).items() if (len(cells) >= min_, True)[min_ == None] and (len(cells) <= max_, True)[max_ == None]}

def count(cell_list):
    if cell_list:
        return {x:[cell for cell in cell_list if x in cell.c] for x in cell_union(cell_list)}
    return {}

def locations(pivot, cell_list, occurance, value):
        cells = has_count(cell_list,occurance, occurance).get(value,[])
        if pivot in cells:
            return cells[:cells.index(pivot)]+cells[cells.index(pivot)+1:]
        return []
        #return {value:cells[:cells.index(pivot)]+cells[cells.index(pivot)+1:] for value,cells in has_count(cell_list,occurance, occurance).items() if pivot in cells}

def strong_links(board,cell,occurance,value):
    locations_row = locations(cell,board.get_row(cell.i).tolist(),occurance, value)
    locations_col = locations(cell,board.get_col(cell.j).tolist(),occurance, value)
    locations_box = locations(cell,board.get_box(cell.k).tolist(),occurance, value)
    return list(set(locations_row+locations_col+locations_box))
    #return {value:list(set(locations_row.get(value,[])+locations_col.get(value,[])+locations_box.get(value,[]))) for value in set(locations_row.keys()+locations_col.keys()+locations_box.keys())}

def weak_links(board,cell,value):
    return [weakcell for weakcell in board.get_row(cell.i).tolist()+board.get_col(cell.j).tolist()+board.get_box(cell.k).tolist() if value in weakcell.c and cell != weakcell]


def visible_intersection(board, cell_list):
    visible = set()
    for i,cell in enumerate(cell_list):
        if i == 0:
            visible = set(board.get_row(cell.i).tolist() + board.get_col(cell.j).tolist() + board.get_box(cell.k).tolist())
        else:
            visible &= set(board.get_row(cell.i).tolist() + board.get_col(cell.j).tolist() + board.get_box(cell.k).tolist())
    for cell in cell_list:
        visible.discard(cell)
    return visible

def share_unit(cell1, cell2):
    return cell1.i == cell2.i or cell1.j == cell2.j or cell1.k == cell2.k

def remove(cell_list,remove):
    if cell_list and remove:
        return [cell for cell in cell_list if cell not in remove]
    return cell_list
