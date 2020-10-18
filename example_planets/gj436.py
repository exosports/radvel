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
    radvel.prior.HardBounds('logk1', 2.5, 3.0),

    radvel.prior.PrimaryTransitPrior(1, 2458362.95999, 0.00010),
    radvel.prior.PrimaryTransitPrior(1, 2454661.50289, 0.00013),
    radvel.prior.PrimaryTransitPrior(1, 2458886.4506827453, 0.00075),
    radvel.prior.PrimaryTransitPrior(1, 2458878.5281523624, 0.00073),
    radvel.prior.PrimaryTransitPrior(1, 2458870.5935419793, 0.00089),
    radvel.prior.PrimaryTransitPrior(1, 2458619.419770181, 0.00085),
    radvel.prior.PrimaryTransitPrior(1, 2458582.403438505, 0.00072),
    radvel.prior.PrimaryTransitPrior(1, 2458566.540817792, 0.0008),
    radvel.prior.PrimaryTransitPrior(1, 2458566.5363777913, 0.00086),
    radvel.prior.PrimaryTransitPrior(1, 2458545.3976668473, 0.0009),

    radvel.prior.SecondaryEclipsePrior(1, 2454496.48567, 0.00290),
    radvel.prior.SecondaryEclipsePrior(1, 2456868.07879, 0.00125),
    radvel.prior.SecondaryEclipsePrior(1, 2454499.12522, 0.00674),
    radvel.prior.SecondaryEclipsePrior(1, 2455585.74037, 0.02775),
    radvel.prior.SecondaryEclipsePrior(1, 2456881.30441, 0.00868),
    radvel.prior.SecondaryEclipsePrior(1, 2457079.57260, 0.00831),
    radvel.prior.SecondaryEclipsePrior(1, 2454501.79592, 0.01620),
    radvel.prior.SecondaryEclipsePrior(1, 2454282.33453, 0.00179),
    radvel.prior.SecondaryEclipsePrior(1, 2454628.68412, 0.00348),
    radvel.prior.SecondaryEclipsePrior(1, 2454631.32678, 0.00323),
    radvel.prior.SecondaryEclipsePrior(1, 2454633.97148, 0.00431),
    radvel.prior.SecondaryEclipsePrior(1, 2454636.61829, 0.00840),
    radvel.prior.SecondaryEclipsePrior(1, 2454858.70792, 0.00943),
    radvel.prior.SecondaryEclipsePrior(1, 2454861.34733, 0.00495),
    radvel.prior.SecondaryEclipsePrior(1, 2454863.99421, 0.00228),
    radvel.prior.SecondaryEclipsePrior(1, 2454866.62937, 0.00724),
    radvel.prior.SecondaryEclipsePrior(1, 2454477.98123, 0.00149),
    radvel.prior.SecondaryEclipsePrior(1, 2454470.05344, 0.01017),
    radvel.prior.SecondaryEclipsePrior(1, 2458361.86068, 0.00975),
    radvel.prior.SecondaryEclipsePrior(1, 2458364.53288, 0.00371),
    radvel.prior.SecondaryEclipsePrior(1, 2454660.41980, 0.00174), 
    radvel.prior.SecondaryEclipsePrior(1, 2454663.05453, 0.00487)
 
]




# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.452, mstar_err=0.012)
