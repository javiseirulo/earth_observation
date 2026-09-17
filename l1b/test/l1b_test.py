# Cross validate L10 OUTPUTS EQUALIZED



# PLOT FROM YOUR OUTPUTS THE EQUALISED OUTPUT VERSUS NOT EQUALISED VERSUS THE TRUTH
# TRUTH = EODP-TS-L1B\input\ism_toa_isrf_VNIR-0.nc


import os
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# path settings
base_folder = '/Users/javi/Documents/Javi/Ingenieria_Aeroespacial/MISE/EarthObservation/drive-download-20260910T163359Z-1-001/EODP_TER_2021/EODP-TS-L1B/'
ref_folder = os.path.join(base_folder, "output")
test_folder = os.path.join(base_folder, "output_test_equalized")
input_folder = os.path.join(base_folder, "input")
not_eq_folder = os.path.join(base_folder, "output_test_not_equalized")

# band and row used for the plot
plot_band = "VNIR-0"
plot_row = 1

# max mismatched values to print per variable
max_print_errors = 5


def load_file_variables(file_path):
    # read all variables from a netcdf file into a dictionary
    content = {}
    with Dataset(file_path, "r") as src:
        for key in src.variables:
            content[key] = src.variables[key][:]
    return content


def check_variable(name, arr_test, arr_ref):
    # check if dimensions match
    if arr_test.shape != arr_ref.shape:
        return False, f"  [{name}] fail: shapes do not match -> {arr_test.shape} vs {arr_ref.shape}"

    # check if data types match
    if arr_test.dtype != arr_ref.dtype:
        return False, f"  [{name}] fail: dtypes do not match -> {arr_test.dtype} vs {arr_ref.dtype}"

    # check if all values are identical (handling nan values safely)
    is_float = np.issubdtype(arr_ref.dtype, np.floating)
    if np.array_equal(arr_test, arr_ref, equal_nan=is_float):
        return True, f"  [{name}] ok: identical"

    # find where the arrays differ
    diff_mask = arr_test != arr_ref
    # ensure nan == nan is not marked as difference
    if is_float:
        both_nan = np.isnan(arr_test) & np.isnan(arr_ref)
        diff_mask = diff_mask & (~both_nan)

    bad_coords = np.argwhere(diff_mask)
    count = len(bad_coords)
    total = arr_ref.size
    ratio = (count / total) * 100

    msg = [f"  [{name}] fail: {count}/{total} values mismatch ({ratio:.3f}%)"]

    # show a few example differences
    for coord in bad_coords[:max_print_errors]:
        idx = tuple(coord)
        msg.append(f"    at {idx}: test={arr_test[idx]} | ref={arr_ref[idx]}")

    if count > max_print_errors:
        msg.append(f"    ... and {count - max_print_errors} more differences")

    return False, "\n".join(msg)


def run_comparison():
    # get list of netcdf files from both directories
    test_files = sorted([f for f in os.listdir(test_folder) if f.endswith(".nc")])
    ref_files = set([f for f in os.listdir(ref_folder) if f.endswith(".nc")])

    target_files = [f for f in test_files if f in ref_files]
    missing_files = [f for f in test_files if f not in ref_files]

    print("starting file comparison")
    print(f"files found to compare: {len(target_files)}")
    if missing_files:
        print(f"files missing in ref folder: {missing_files}")
    print("-" * 50)

    overall_success = True
    summary_list = []

    # iterate through each shared file
    for filename in target_files:
        print(f"\nchecking: {filename}")
        data_test = load_file_variables(os.path.join(test_folder, filename))
        data_ref = load_file_variables(os.path.join(ref_folder, filename))

        file_success = True

        # verify that each reference variable exists and matches
        for var_name in data_ref:
            if var_name not in data_test:
                print(f"  [{var_name}] fail: missing variable in test file")
                file_success = False
                continue

            matches, report = check_variable(var_name, data_test[var_name], data_ref[var_name])
            print(report)
            if not matches:
                file_success = False

        # warn about any extra variables
        extras = [v for v in data_test if v not in data_ref]
        if extras:
            print(f"  note: extra variables found in test: {extras}")

        summary_list.append((filename, file_success))
        if not file_success:
            overall_success = False

    # print final results
    print("\n" + "=" * 50)
    print("summary")
    for fname, ok in summary_list:
        status = "pass" if ok else "fail"
        print(f"[{status}] {fname}")

    print("-" * 50)
    if overall_success:
        print("final verdict: all files matched perfectly")
    else:
        print("final verdict: differences detected")
    print("=" * 50)


def read_toa(file_path):
    # read the "toa" variable from a netcdf file
    with Dataset(file_path, "r") as src:
        toa = np.array(src.variables["toa"][:])
    return toa


def plot_equalization_effect(band, row):
    # build the three file paths to compare
    input_file = os.path.join(input_folder, f"ism_toa_isrf_{band}.nc")
    not_eq_file = os.path.join(not_eq_folder, f"l1b_toa_{band}.nc")
    eq_file = os.path.join(test_folder, f"l1b_toa_{band}.nc")

    # read one row (across track) of each toa
    toa_input = read_toa(input_file)[row, :]
    toa_not_eq = read_toa(not_eq_file)[row, :]
    toa_eq = read_toa(eq_file)[row, :]

    # act pixel axis
    act_pixels = np.arange(len(toa_input))

    # plot the three curves together
    plt.figure(figsize=(10, 5))
    plt.plot(act_pixels, toa_input, color="blue", label="input (truth, ism_toa_isrf)")
    plt.plot(act_pixels, toa_not_eq, color="red", label="l1b toa, not equalized")
    plt.plot(act_pixels, toa_eq, color="black", label="l1b toa, equalized")

    plt.title(f"effect of the equalization for {band}, row {row}")
    plt.xlabel("act pixel [-]")
    plt.ylabel("toa [mW/m2/sr]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    out_path = os.path.join(test_folder, f"equalization_effect_{band}.png")
    plt.savefig(out_path)
    print(f"plot saved to: {out_path}")
    plt.show()


if __name__ == "__main__":
    run_comparison()
    plot_equalization_effect(plot_band, plot_row)
