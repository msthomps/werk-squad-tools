import pandas as pd
import numpy as np
import random

def SFR_testVals(Ha_Lum_array, SFR_array, SFR_flags):
    """ 
    Recalculate SFR values from a random index and compare the previous calculation of the same index
    -------------------------------------------
    Method:
        The index is chosen using the random package which employs Mersenne Twister as its random number generator
        See doc here: https://docs.python.org/3/library/random.html#module-random
        
        The comparision is done with numpy isclose() method
        See doc here: https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.isclose.html
    ------------------------------------------
    Args:
        All inputs should be numpy nd.arrays
    ------------------------------------------    
    Returns:
        True = the values are within a tolerance of 1E-8 of each other (bool)
        False = the values have failed a tolerance check of 1E-8 (bool)
    """
    # Select random index to recalc SFR
    pull_num = random.randint(0., len(Ha_Lum_array))
    Ha_val = Ha_Lum_array[pull_num]
    SFR_check = 7.9e-42 * Ha_val
    # Pull the same index from the SFR calculations array
    SFR_val = SFR_values[pull_num]
    compare = np.isclose(SFR_check, SFR_val, 1E-8)    
    return compare

def SFR_testFlag(All_calc_df):
    """ 
    Pull a random index and test that the condition is met for the flag it's identified with.
    e.g. Was SFR calculated from Halpha flux (flag = 'Ha') or Hbeta flux (flag = 'Ha')
    -------------------------------------------
    Method:
        The index is chosen using the random package which employs Mersenne Twister as its random number generator
        See doc here: https://docs.python.org/3/library/random.html#module-random
    ------------------------------------------
    Args:
        Pandas DataFrame: containing all calculations and flags
    ------------------------------------------    
    Returns:
        Statement of which flag it tested and if the coniditon was passed or failed (str)
    """
    pull_num = random.randint(0., len(test))
    SFR_flag = SFR_flags[pull_num]
    if All_calc_df.SFR_Flag == 'Ha' & All_calc_df.Halpha_LQ != 1:
        return "Ha condition failed"
    else:
        return "Ha condition passed"
    if All_calc_df.Halpha_Lum_Flag == 'Hb' & All_calc_df.Hbeta_LQ != 1 & All_calc_df.Halpha_LQ < 2 & All_calc_df.Halpha_LQ > 0:
        return False "Hb condition failed"
    else:
        return True "Hb condition passed"