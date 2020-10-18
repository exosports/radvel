# Example Keplerian fit configuration file

# Required packages for setup
import os
import pandas as pd
import numpy as np
import radvel

starname  = 'K2-24'                            # star name is K2-24.
num_planets  = 2                                  # K2-24 is a system with only 2 planets.
instnames = ['hires']                          # inst used is the keck/hires.
ntels     = len(instnames)                     # will just be 1. Being hires is the only inst.
fitting_basis = 'logper tc secosw sesinw k'    # chosen fitting basis is the smae used in Petigura et al 2018.analysis.
bjd0 = 0                                       # reference epoch.
planet_letters = {1: 'b', 2: 'c'}              # map the numbers in the Parameters keys to planet letters (for plotting and tables).

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(num_planets,basis = 'per tc e w k', planet_letters = planet_letters)   

# K2-24b
anybasis_params['per1'] = radvel.Parameter(value = 20.8851)          # period.
anybasis_params['tc1']  = radvel.Parameter(value = 2450965.7948)     # time of inferior conjunction.
anybasis_params['e1']   = radvel.Parameter(value = 0.06)             # eccentricity.
anybasis_params['w1']   = radvel.Parameter(value = np.pi/2.)         # argument of periastron of the star's orbit. 
anybasis_params['k1']   = radvel.Parameter(value = 4.5)              # velocity semi-amplitude

# K2-24c
anybasis_params['per2'] = radvel.Parameter(value = 42.36342)         # same parameters for c.
anybasis_params['tc2']  = radvel.Parameter(value = 2456915.6251)
anybasis_params['e2']   = radvel.Parameter(value = 0)
anybasis_params['w2']   = radvel.Parameter(value = np.pi/2.)
anybasis_params['k2']   = radvel.Parameter(value = 4.6)

anybasis_params['dvdt'] = radvel.Parameter(value=0.0)        # slope: (If rv is m/s and time is days then [dvdt] is m/s/day)
anybasis_params['curv'] = radvel.Parameter(value=0.0)        # curvature: (If rv is m/s and time is days then [curv] is m/s/day^2)

# analytically calculate gamma if vary=False and linear=True
anybasis_params['gamma_hires'] = radvel.Parameter(value = 0.1, vary = False, linear = True)      
anybasis_params['gamma_tr']    = radvel.Parameter(value = 0.0, vary = False)
anybasis_params['gamma_ecl']   = radvel.Parameter(value = 0.0, vary = False)

anybasis_params['jit_hires'] = radvel.Parameter(value = 0)        
anybasis_params['jit_tr']    = radvel.Parameter(value = 0, vary = False)
anybasis_params['jit_ecl']   = radvel.Parameter(value = 0, vary = False)

anybasis_params['ti'] = radvel.Parameter(value = 2100, vary = False)
anybasis_params['tf'] = radvel.Parameter(value = 2500, vary = False)  

# Convert input orbital parameters into the fitting basis
params = anybasis_params.basis.to_any_basis(anybasis_params,fitting_basis)

# RV data.
data   = pd.read_csv(os.path.join(radvel.DATADIR,'k2-24_rv.txt'), sep=' ') 

# Transit data.
trdata = pd.read_csv(os.path.join(radvel.DATADIR,'k2-24_tr.txt'), sep=' ')   

# No Ecl data for K2-24.

# timebase defined as the average of the min rv and max rv.
time_base = 2367.852646

# No defined priors beside eccentricity.
priors = [

    radvel.prior.EccentricityPrior( num_planets ),
    radvel.prior.HardBounds( per1, 
#name, min, max
#keep within factor of 2     
]

# stellar mass and mass err taken from Petigura 2018.
stellar = dict(mstar = 1.07, mstar_err = 0.06)

