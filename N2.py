import numpy as np
import pandas as pd

def N2(F_N, F_Ha):
    
    '''
    This function will calculate the flux ratio of Nitrogen II (6583) and H_alpha
    
    F_N = flux of Nitrogen II
    F_Ha = Flux of H_alpha
    '''
    
    n2 = F_N / F_Ha
    
    return n2
