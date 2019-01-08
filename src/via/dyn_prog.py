'''
Created on Jan 7, 2019

@author: paepcke
'''

import numpy as  np
import pandas as pd
from via.point import Point


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


    def __init__(self, mtx, start_pt, end_pt):
        '''
        Constructor
        '''
        self.best_path(mtx, start_pt, end_pt)
        
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
        left = mtx.iloc[i,j-1]
        diag = mtx.iloc[i-1,j-1]
        up   = mtx.iloc(i-1,j)
        
        if optimization == Opt.Max:
            maximize = True,
        else:
            maximize = False,
            
        best = max([left, diag, up]) if maximize else min([left, diag, up])  
        if best == left:
            return (Point(i, j-1), best)
        
        if best == diag:
            return (Point(i-1, j-1), best)
        
        else:
            return(Point(i-1, j), best)
        
    
# ------------------ Main -----------------

if __name__ == '__main__':
    
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
    DynSolver(m, p_start, p_end, Opt.Max)