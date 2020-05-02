import pandas as pd
import numpy as np

def O3HB(F_O, F_Hb):
    
    '''
    This function will calculate the flux ratio of Oxygen III (5007) and H_beta
    ---------------------------------------------------------------------------
    F_O = flux of oxygen III
    F_Hb = flux of H_beta
    ---------------------------------------------------------------------------
    '''
    
    O3Hb = F_O / F_Hb
    
    return O3Hb
