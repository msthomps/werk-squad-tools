#!/usr/bin/env python
# coding: utf-8

# In[25]:


import numpy as np


# In[26]:


#Function simply takes in an array of calculated N2 values, i.e. the flux ratio of [NII] 6583 to Halpha 6563.

#Called from the switchboard for conditions when log (O3HB/N2)>1.9 i.e. [O3N2]>1.9

def logN2_metallicity(N2):
    iterable = ((8.92+(0.57*np.log10(N2[i]))) for i in range(len(N2)))
    N2_metallicity=np.fromiter(iterable, np.float64)
    return N2_metallicity


# In[27]:


#### Alt method :

# def logN2_metallicity1(N2):
#     m=[]
    
#     for i in range(len(N2)):
#         m.append(i)
#         if (~np.isnan(N2[i])):
#             m[i]=np.float(8.92+(0.57*np.log10(N2[i])))
#         else:
#             m[i]=np.nan
#         i+=1    
#     return m


