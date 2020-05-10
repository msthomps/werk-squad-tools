from astropy.cosmology import FlatLambdaCDM
import numpy as np
import pandas as pd
import os
from os.path import expanduser
from glob import glob
from O3N2 import*
from SFR import*
from Distance import*
from Ha_Luminosity import*
from findR23 import*
from O3HB import*
from N2 import*
from Pettini_Pagel_N2 import*

# 'galaxy' is a data table of Final_galinfo.csv file which 
# is a subset of data from the galaxyinfo.xlsx data from CGM^2
txt_in = input("Please input Filepath: ")
galaxy = pd.read_csv(txt_in)
galaxy.to_numpy()   

# This 'for' loop will look for '-99' values and change them to 'NaN' values.
columns = np.array(galaxy.columns)
for i in columns:
    n = 0
    while n < len(galaxy):
        if galaxy[i][n] == -99.0:
            galaxy[i][n] = np.nan
        n += 1 
        
# Calculate distance
galaxy['Distance'] = Distance(galaxy['z'])

# Calculate Halpha Luminosity, using Halpha_flux and 2.86(Hbeta_flux)
Hbeta = 2.86*galaxy['Hbeta_flux']
galaxy['Ha_luminosity'] = Ha_luminosity(galaxy['Distance'],Hbeta)

gala_Ha = Ha_luminosity(galaxy['Distance'],galaxy['Halpha_flux'])
galaxy_Ha = gala_Ha > 0.0
g = galaxy['Ha_luminosity']
g[galaxy_Ha] = gala_Ha

# Calculating SFR using Halpha luminosity
galaxy['SFR_WS'] = SFR(galaxy['Ha_luminosity'])
galaxy['SFR_flag'] = SFR_switchboard(galaxy)

# Calculate 'O3HB'
galaxy['O3HB'] = O3HB(galaxy['OIII_flux'],galaxy['Hbeta_flux'])

# Calculate 'N2'
galaxy['N2'] = N2(galaxy['NII_flux'],galaxy['Halpha_flux'])

# Calculate 'O3N2'
galaxy['O3N2'] = O3N2(galaxy)

# Calculate 'Z_O3N2L'
galaxy['Z_O3N2L'] = Z_O3N2L(galaxy)

# Calculate where 'O3N2' > 1.9, as well as where 'N2' exists but 'O3N2' does not
no_N2_Z = (galaxy['Z_O3N2L'] > 0.0) & (galaxy['O3N2'] < 1.9)
N2_Z = logN2_metallicity(galaxy['N2'])
N2_Z[no_N2_Z] = np.nan
galaxy['Z_O3N2H'] = N2_Z

# Now let's merge with another dataframe, mainly to bring in some mass values.
# We'll be using the same code that Steven Bett used from his jupyter notebook
# on Dropbox: Dropbox/IGM_spectra/jupyter_notebooks_SB/SFR+Metal_CGM2.ipynb
# Mass and Friends
# filepath for table containing stellar masses for all the galaxies that we've been working with:
home = expanduser('~')
path = os.path.join(home,'Dropbox','**','cgmsq_allsurveys_cgmsystable.fits')
massfilepath = glob(path, recursive=True)
# Extracts table from fits file and resolves various issues 
# required to concatenate this new table 
# (which Matt made at some point previously) with our new SFR info-containing table.
mass_and_friends = Table.read(massfilepath[-1])
mass_and_friends.remove_columns(['zRR', 'zRR_Err', 'spectype_rr'])
mass_and_friends = mass_and_friends.to_pandas()
mass_and_friends['id'] = mass_and_friends['id'].str.decode('utf-8')
# merges mass table with initial (SFR-containing) one:
galaxy = pd.merge(galaxy, mass_and_friends, on=['id'], how='right')
# sorting out some (more) naming conflicts:
galaxy.rename(columns={'z_x': 'z'}, inplace=True)

# Calculate R23
r23 = findR23(galaxy['OII_flux'],galaxy['OIII_flux'],galaxy['NII_flux'],galaxy['Halpha_flux'],
             galaxy['Hbeta_flux'],galaxy['mstars'])
galaxy['Z_R23'] = r23[0]
galaxy['Z_R23_flag'] = r23[1]

# Now we'll create a 'Z_Flag' column for our data to rate the Metallicity based on how it is 
# calculated.
# Defining the 'Z_flag' column
z_flag = np.array((len(galaxy))*[np.nan], dtype=object)  
# Flagging metallicity calculated with R23
three = galaxy['Z_R23'] > 0.0
z_flag[three] = 'R23'
# Flagging metallicity calculated with N2 (and some O3N2 calculations mixed in, but we'll
# re-flag those next).
two = galaxy['Z_O3N2H'] > 0.0
z_flag[two] = 'N2'
# Flagging metallicity calculated with O3N2
one = (galaxy['Z_O3N2L'] > 0.0) | (galaxy['O3N2'] > 1.9)
z_flag[one] = 'O3N2'
galaxy['Z_Flag'] = z_flag

# This next part is just to rename some columns that may conflict. We will name the column where
# SFR was calculated by Werk SQuAD 'SFR' and the column where SFR was calculated using photometry (CIGALE)
# 'SFR_photo' 
galaxy.rename(columns={'SFR':'SFR_photo'}, inplace=True)
galaxy.rename(columns={'SFR_WS':'SFR'}, inplace=True)

# Finally we'll save the data to the directory of th eusers liking.
txt_out = input("Please input filepath and name to save to: ")
galaxy.to_csv(txt_out, index=False)
print('Thank you.')

#print(galaxy)