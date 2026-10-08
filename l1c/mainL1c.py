
# MAIN FUNCTION TO CALL THE L1C MODULE


import os


# Directory - this is the common directory for the execution of the E2E, all modules
# Paths are resolved relative to the repository root so the module runs from any cwd.
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from l1c.src.l1c import l1c

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = os.path.join(rootdir, 'auxiliary')
# GM dir + L1B dir
indir = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-L1C/input/gm_alt100_act_150,/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-L1C/input/l1b_output'
outdir = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-L1C/output_javi'

# Initialise the ISM
myL1c = l1c(auxdir, indir, outdir)
myL1c.processModule()
