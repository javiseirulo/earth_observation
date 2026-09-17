
# MAIN FUNCTION TO CALL THE ISM MODULE

from ism.src.ism import ism

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/earth_observation/auxiliary'
indir = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-ISM/input/gradient_alt100_act150'
outdir = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-ISM/output_test'

# Initialise the ISM
myIsm = ism(auxdir, indir, outdir)
myIsm.processModule()
