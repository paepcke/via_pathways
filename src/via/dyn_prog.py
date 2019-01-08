'''
Created on Jan 7, 2019

@author: paepcke

Solving
https://www.geeksforgeeks.org/min-cost-path-dp-6/

'''

import numpy as  np
import pandas as pd
from via.point import Point
from numpy.ma.testutils import assert_equal


class Opt(enumerate):
    Max = 1
    Min = 2

class DynSolver(object):
    '''
    classdocs
    '''

    #-------------------------
    # Constructor 
    #--------------


    def __init__(self, mtx, start_pt, end_pt, optimization):
        '''
        Constructor
        '''
        self.path_weight = self.best_path(mtx, start_pt, end_pt, optimization)
        
    #-------------------------
    # best_path 
    #--------------
        
    def best_path(self, mtx, start_pt, end_pt, optimization):
        
        #print(mtx)
        cum_weight   = [mtx.iloc[end_pt.x, end_pt.y]]
        curr_pt = end_pt 
        
        while curr_pt != start_pt: 
            (curr_pt, incr_weight) = self.lowest_back_one(mtx, 
                                                               curr_pt.x, 
                                                               curr_pt.y,  
                                                               optimization)
            cum_weight.insert(0, incr_weight)

        return sum(cum_weight)     

    #-------------------------
    # best_back_one 
    #--------------
            
    def lowest_back_one(self, mtx, i, j, optimization):

        # Convenience var to avoid repeated '==' expression below:        
        if optimization == Opt.Max:
            _maximize = True
        else:
            _maximize = False

        # Init to None so we know later on when we
        # did not set a value for left/diag/up, because
        # the cells were on the edge:
        left = diag = up = None
        
        # Get values to the left, above, and diagonal:
        if j>0:
            left = mtx.iloc[i,j-1]

        if i>0 and j>0:        
            diag = mtx.iloc[i-1,j-1]
            
        if i>0:
            up   = mtx.iloc[i-1,j]
        
        # Remove weight that are None, because we were
        # at an edge:            
        available_bests = [best_val for best_val in [left, diag, up] if best_val is not None]
        
        # 'Best' depends on whether we are maximizing or minimizing:
        best = max(available_bests) if _maximize else min([left, diag, up])  
        if best == left:
            return (Point([i, j-1]), best)
        
        if best == diag:
            return (Point([i-1, j-1]), best)
        
        else:
            return(Point([i-1, j]), best)
    
# ------------------ Main -----------------

if __name__ == '__main__':
    
    # Only up, left, and diag allowed:
    data = np.array([[1,2,3],
                     [4,8,2],
                     [1,5,3]
                    ]) 
    m = pd.DataFrame(data=data,
                     index=['C1','C2', 'C3'],
                     columns=['C1','C2', 'C3']
                     )
    
    p_start = Point([0,0])
    p_end   = Point([2,2])

    # Minimize path
    solver = DynSolver(m, p_start, p_end, Opt.Min)
    print('Sum: {}'.format(solver.path_weight))
    assert_equal(solver.path_weight, 8)

    # Maximize path
    solver = DynSolver(m, p_start, p_end, Opt.Max)
    print('Sum: {}'.format(solver.path_weight))
    assert_equal(solver.path_weight, 16)
