import pandas as pd
import numpy as np
from astropy import constants as const
from astropy import units as u
from astropy.cosmology import FlatLambdaCDM

def SFR(Ha_array):
    """ 
    Calculate distance using H-alpha luminosity.
    -------------------------------------------
    Method:
        Distance calc made using astropy.cosmology packages cosmo.luminosity_distance() method
        See documentation here: https://docs.astropy.org/en/stable/cosmology/
    ------------------------------------------
    Args:
        Numpy nd.array of H-alpha Luminosities
    ------------------------------------------    
    Returns:
        Numpy nd.array
    """
    SFR = np.array([])
    SFR_calc = [((7.9e-42) * i) for i in Ha_array]
    SFR = np.append(SFR, SFR_calc)
    return SFR

def SFR_switchboard(lines_df):
    """ 
    Assign flags based on which lines are used to calculate SFR/ H-alpha Luminosity
    if Flag = 'NaN' -- No determination
            = 'Ha' -- H-alpha lines used 
            = 'Hb' -- H-beta lines used
    -------------------------------------------
    Method Assumed for SFR/H-alpha Lum calculations:
        Ha_Lum_Ha = (LQ_cut_Ha['Halpha_flux']) * (4 * np.pi * (LQ_cut_Ha['Distance_cm'])**2)
        Ha_Lum_Hb = ((LQ_cut_Hb['Hbeta_flux']) * 2.86) * (4 * np.pi * (LQ_cut_Hb['Distance_cm'])**2)
        Where LQ_cut_* corresponds to using the respective *_cond written in this function
        
        SFR = ((7.9e-42) * Ha_Lum)
    ------------------------------------------
    Args:
        DataFrame containing Line Quality information for H-alpha and H-beta
    ------------------------------------------    
    Returns:
        3 numpy.ndarray (arrays = Flags, Ha indices, Hb indices), all entries dtype = str
    """
    # Make integers for conditionals
    lines_df.Halpha_LQ.astype('Int64')
    lines_df.Hbeta_LQ.astype('Int64')
    # Conditions for each calc
    Ha_cond = (lines_df['Halpha_LQ']>0) & (lines_df['Halpha_LQ']<2) 
    Hb_cond = (lines_df['Hbeta_LQ']>0) & (lines_df['Hbeta_LQ']<2) & (lines_df['Halpha_LQ']!=1)
    # Make flags
    SFR_flags = np.full(len(lines_df), str(np.nan))
    SFR_flags[Ha_cond] = 'Ha'
    SFR_flags[Hb_cond] = 'Hb'
    return SFR_flags