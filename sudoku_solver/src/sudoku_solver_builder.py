'''
Created on Jan 13, 2013

@author: Brad
'''

class SudokuSolverBuilder():
    def __init__(self, board, solver_list):
        self.board = board
        self.solver_list = solver_list
        
    def solve(self):
        solvers_used = {}
        while True:
            for i, solver in enumerate(self.solver_list):
                if i == 0 or i == 1:
                    solved_sets = solver.solve(self.board, do_all=True)
                else:
                    solved_sets = solver.solve(self.board, do_all=False)
                for solved_set in solved_sets:
                    print solved_set
                    solvers_used[str(solved_set.solver)] = solvers_used.get(str(solved_set.solver), 0) + 1
                if solved_sets:
                    break
            if (i >= len(self.solver_list) - 1 and not solved_sets) or self.board.errors() or self.board.solved():
                break
        print solvers_used