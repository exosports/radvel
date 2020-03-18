import os
import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = 'GJ436'
nplanets = 1    # number of planets in the system
instnames = ['harps', 'hires', 'carmenes']    # list of instrument names. Can be whatever you like (no spaces) but should match 'tel' column in the input file.
ntels = len(instnames)       # number of instruments with unique velocity zero-points
fitting_basis = 'per tc secosw sesinw logk'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 0   # reference epoch for RV timestamps (i.e. this number has been subtracted off your timestamps)
planet_letters = {1: 'b'}   # map the numbers in the Parameters keys to planet letters (for plotting and tables)


# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(nplanets,basis='per tc e w k', planet_letters=planet_letters)    # initialize Parameters object

anybasis_params['per1'] = radvel.Parameter(value=2.64394)      # period of 1st planet
anybasis_params['tc1'] = radvel.Parameter(value=2454222.61588)     # time of transit of 1st planet
anybasis_params['e1'] = radvel.Parameter(value=0.170115)          # eccentricity of 1st planet
anybasis_params['w1'] = radvel.Parameter(value=-0.648143)      # argument of periastron of the star's orbit for 1st planet
anybasis_params['k1'] = radvel.Parameter(value=17.3946)          # velocity semi-amplitude for 1st planet

time_base = 2455000          # abscissa for slope and curvature terms (should be near mid-point of time baseline)
anybasis_params['dvdt'] = radvel.Parameter(value=0.0)         # slope: (If rv is m/s and time is days then [dvdt] is m/s/day)
anybasis_params['curv'] = radvel.Parameter(value=0.0)        # curvature: (If rv is m/s and time is days then [curv] is m/s/day^2)

# analytically calculate gamma if vary=False and linear=True
anybasis_params['gamma_harps']    = radvel.Parameter(value=9789.2, vary=False, linear=True)       # velocity zero-point for hires_rk
anybasis_params['gamma_hires']    = radvel.Parameter(value=   0.1, vary=False, linear=True)       # "                   "   hires_rj
anybasis_params['gamma_carmenes'] = radvel.Parameter(value= -19.7, vary=False, linear=True)       # "                   "   hires_apf
anybasis_params['gamma_tr']       = radvel.Parameter(value=   0.0, vary=False)
anybasis_params['gamma_ecl']      = radvel.Parameter(value=   0.0, vary=False)

anybasis_params['jit_harps']    = radvel.Parameter(value=0)         # jitter for hires_rk
anybasis_params['jit_hires']    = radvel.Parameter(value=0)         # "      "   hires_rj
anybasis_params['jit_carmenes'] = radvel.Parameter(value=0)         # "      "   hires_apf
anybasis_params['jit_tr']       = radvel.Parameter(value=0, vary=False)
anybasis_params['jit_ecl']      = radvel.Parameter(value=0, vary=False)

anybasis_params['ti'] = radvel.Parameter(value=2450000, vary=False)
anybasis_params['tf'] = radvel.Parameter(value=2460000, vary=False)

# Convert input orbital parameters into the fitting basis
params = anybasis_params.basis.to_any_basis(anybasis_params,fitting_basis)

# Set the 'vary' attributes of each of the parameters in the fitting basis. A parameter's 'vary' attribute should
# be set to False if you wish to hold it fixed during the fitting process. By default, all 'vary' parameters
# are set to True.
#params['dvdt'].vary = False
#params['curv'].vary = False
#params['jit_harps'].vary = False
#params['jit_hires'].vary = False
#params['jit_carmenes'].vary = False
#params['secosw1'].vary = False
#params['sesinw1'].vary = False
#params['per1'].vary = False
#params['tc1'].vary = False

# Load radial velocity data, in this example the data is contained in
# an ASCII file, must have 'time', 'mnvel', 'errvel', and 'tel' keys
# the velocities are expected to be in m/s
data   = pd.read_csv(os.path.join(radvel.DATADIR,'gj436-rv.txt'), sep=' ')

# Transit data
trdata = pd.read_csv(os.path.join(radvel.DATADIR,'gj436-tr.txt'), sep=' ')

# Ecl data
ecldata = pd.read_csv(os.path.join(radvel.DATADIR,'gj436-ecl.txt'), sep=' ')

# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior( nplanets ),           # Keeps eccentricity < 1
    radvel.prior.HardBounds('per1', 2.6, 2.7),
    radvel.prior.HardBounds('logk1', 2.5, 3.0)
]


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.452, mstar_err=0.012)
