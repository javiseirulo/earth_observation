
# MAIN FUNCTION TO CALL THE L1B MODULE

import os

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
# Paths are resolved relative to the repository root so the module runs from any cwd.
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

auxdir = os.path.join(rootdir, 'auxiliary')
indir = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-L1B/input'
outdir = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-L1B/output_test_equalized'

os.makedirs(outdir, exist_ok=True)

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)  # instance of the class l1b, which is under /Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/earth_observation/l1b/src/l1b.py
myL1b.processModule()
