import subprocess
from pathlib import Path
from itertools import product
from functools import reduce
import numpy as np
import re
import argparse
import threading
import os
from netCDF4 import Dataset
import random
import json

def run_fortran_executable(executable_path, input_params: tuple, input_indices: tuple = None, output_mask = None, BLOCK=True, LOG=False):
    """
    Runs a Fortran executable with an input file and writes output to an output file.
    
    Args:
    - executable_path (str or Path): Path to the Fortran executable.
    - input_file (str or Path): Path to the input file to provide via stdin.
    - output_file (str or Path): Path where stdout will be written.
    """
    # ASDF = False
    # if random.random() < 0.01:
    #     ASDF = True
    # if ASDF:
    #     print(input_params, input_indices)
    sza, vza, raa, aod, band = input_params
    input_text = create_input_text(sza, vza, raa, aod, band)
    # Run the Fortran executable with input redirected from input_text and output to outfile
    # process = subprocess.run(f'./{str(executable_path)}', input=input_text.encode(), stdout=outfile, stderr=subprocess.PIPE, shell=True)
    # if process.returncode != 0:
    #     print(f"Error running {executable_path} with {input_text}")
    #     print(process.stderr.decode())
    
    result = subprocess.run(f'./{str(executable_path)}', input=input_text, capture_output=True, shell=True, text=True, check=True)
    # print(result)
    result = result.stdout.splitlines()
    ratio_values = result[0].split(' ')
    direct_irradiance_ratio, atmospheric_path_reflectance = float(ratio_values[0]), float(ratio_values[3])
    gaseous_transmittance = float(result[1])
    downward_scattering_transmittance, upward_scattering_transmittance = float(result[2]), float(result[3])
    spherical_albedo = float(result[4])
    optical_depth = float(result[5])
    
    if output_mask is not None:
        sza_i, vza_i, raa_i, aod_i, band_i = input_indices
        if BLOCK:
#             if ASDF or band_i == 4:
#                 print(input_params, input_indices)
#                 print(atmospheric_path_reflectance,
# gaseous_transmittance,
# downward_scattering_transmittance,
# upward_scattering_transmittance,
# spherical_albedo,
# optical_depth,
# direct_irradiance_ratio)
            output_mask[0, raa_i, aod_i, band_i] = atmospheric_path_reflectance
            output_mask[1, raa_i, aod_i, band_i] = gaseous_transmittance
            output_mask[2, raa_i, aod_i, band_i] = downward_scattering_transmittance
            output_mask[3, raa_i, aod_i, band_i] = upward_scattering_transmittance
            output_mask[4, raa_i, aod_i, band_i] = spherical_albedo
            output_mask[5, raa_i, aod_i, band_i] = optical_depth
            output_mask[6, raa_i, aod_i, band_i] = direct_irradiance_ratio
        else:
            output_mask[0, sza_i, vza_i, raa_i, aod_i, band_i] = atmospheric_path_reflectance
            output_mask[1, sza_i, vza_i, raa_i, aod_i, band_i] = gaseous_transmittance
            output_mask[2, sza_i, vza_i, raa_i, aod_i, band_i] = downward_scattering_transmittance
            output_mask[3, sza_i, vza_i, raa_i, aod_i, band_i] = upward_scattering_transmittance
            output_mask[4, sza_i, vza_i, raa_i, aod_i, band_i] = spherical_albedo
            output_mask[5, sza_i, vza_i, raa_i, aod_i, band_i] = optical_depth
            output_mask[6, sza_i, vza_i, raa_i, aod_i, band_i] = direct_irradiance_ratio
    
    if LOG:    
        print(f'Simulation results for:\n' + \
                f' sza={sza:.2f}\n' + \
                f' vza={vza:.2f}\n' + \
                f' raa={raa:.2f}\n' + \
                f' aod={aod:.2f}\n' + \
                f' band={band}\n' + \
                '  \\/\n' + \
                f'direct_irradiance_ratio={direct_irradiance_ratio}\n' + \
                f'atmospheric_path_reflectance={atmospheric_path_reflectance}\n' + \
                f'gaseous_transmittance={gaseous_transmittance}\n' + \
                f'downward_scattering_transmittance={downward_scattering_transmittance}\n' + \
                f'upward_scattering_transmittance={upward_scattering_transmittance}\n' + \
                f'spherical_albedo={spherical_albedo}\n' + \
                f'optical_depth={optical_depth}\n---\n')
    
    # with open(output_file, 'r') as outfile:     
    #     all_output_text = outfile.read()
    #     direct_irr_percent_match = re.search(r'%\s*of\s*direct\s*irr.\s*.*\*\s*\*\s*(\d+\.\d*)', all_output_text)
    #     if direct_irr_percent_match:
    #         direct_irr_percent = direct_irr_percent_match.group(1)
    #         print(f'Direct irradiance ratio for:\n' + \
    #             f' sza={sza:.2f}\n' + \
    #             f' vza={vza:.2f}\n' + \
    #             f' raa={raa:.2f}\n' + \
    #             f' aod={aod:.2f}\n' + \
    #             f' band={band}\n' + \
    #             f'={direct_irr_percent}')
    
    
            
def rangef_inc(min, max, step):
    epsilon = step / 100
    return np.linspace(min, max, int((max - min + epsilon) / step) + 1).tolist()

def create_input_text(sza, vza, raa, aod, band):
    _MONTH, _DAY = 4, 28
    text = f'''0 (User defined)
{sza:.2f} 0.0 {vza:.2f} {raa:.2f} {_MONTH} {_DAY} (geometrical conditions)
0  (No Gaseous Absorptio)
1 Continental Model
0
{aod:.2f} value
0 (target level)
-35786 (sensor level)
{band} (chosen band)
0 Homogeneous surface
1 (directional effects)
10 (MODIS operational BDRF)
0.3091 0.1290 0.0762
-1 No atm. corrections selected 
'''
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Fortran executable with parameter combinations")
    parser.add_argument('-d', '--directory', dest='sixs_dir', type=str, default='./fortran', help='6S code directory. Defaults to ./fortran')
    parser.add_argument("--make", action="store_true", default=False, help="Make the 6s executable from scratch.")
    parser.add_argument('--no-save', action='store_true', dest='no_save', default=False, help='Don\'t save to lookup table.')
    args = parser.parse_args()
    
    if not os.path.exists(args.sixs_dir) or not os.path.isdir(args.sixs_dir):
        parser.error(f'{args.sixs_dir} is not a directory or does not exist.')
        
    if args.make:
        subprocess.run(f'cd {args.sixs_dir} && make && make clean && cd ..', shell=True)
        
    # Define paths and list of input files
    executable_path = None
    pattern = re.compile(r".*sixsV\d+\.\d+")
    for file in Path(args.sixs_dir).iterdir():
        if file.is_file() and pattern.fullmatch(file.name):
            executable_path = file
            file.chmod(0o755)
            print(executable_path.name)
            break
        
    if executable_path is None:
        print('Executable for 6S not found. Consider running with --make')
        quit()
    
    # subprocess.run('ls')
    # subprocess.run(f'cd fortran && chmod +x "{executable_path.name}" && cd ..')
        
    with open('./new_srfs.json', 'r') as json_f:
        data = json.load(json_f)
        band_range = range(data['start_band_index'], data['start_band_index'] + len(data['new_srfs']))
        band_names = data['new_srfs']
    
    input_params = [
        rangef_inc(0, 0.75, 0.05), # SZA
        rangef_inc(0, 0.75, 0.05), # VZA
        range(0, 180+1, 30), # RAA
        [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0], # AOD
        band_range
    ]
    
    input_indices = [list(range(len(param))) for param in input_params]

    shape = [len(x) for x in input_params]
    size = reduce(lambda a, c: a * c, shape, 1) * 7
    print('Input shape', shape, size)
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # Run the executable on each input file
    count = 0
    
    nc_filepath = os.path.join(output_dir, 'lutabi.nc')
    if not args.no_save and not os.path.exists(nc_filepath):
        print('Creating NC file')
        with Dataset(os.path.join(output_dir, 'lutabi.nc'), 'w', format='NETCDF4') as nc:
            nc.createDimension('NumVars', 7)
            nc.createDimension('SolarZenithInterval', 16)
            nc.createDimension('ViewZenithInterval', 16)
            nc.createDimension('RelativeAzimuthInterval', 7)
            nc.createDimension('AODInterval', 10)
            nc.createDimension('BandIndex', 5)
            
            sza_var = nc.createVariable('SZA', 'f4', ('SolarZenithInterval',))
            vza_var = nc.createVariable('VZA', 'f4', ('ViewZenithInterval',))
            rai_var = nc.createVariable('RAA', 'f4', ('RelativeAzimuthInterval',))
            aod_var = nc.createVariable('AOD', 'f4', ('AODInterval',))
            band_var = nc.createVariable('band', 'f4', ('BandIndex',))
            table_var = nc.createVariable('Lutvars', 'f4', ('NumVars', 
                                                                'SolarZenithInterval', 
                                                                'ViewZenithInterval', 
                                                                'RelativeAzimuthInterval', 
                                                                'AODInterval', 
                                                                'BandIndex'))
            
            sza_var[:] = np.array(input_params[0])
            vza_var[:] = np.array(input_params[1])
            rai_var[:] = np.array(input_params[2])
            aod_var[:] = np.array(input_params[3])
            band_var[:] = np.array(input_params[4])
            table_var[:] = np.zeros(shape=(7, *(len(param) for param in input_params)))
    
    lut_block = np.zeros(shape=(7, *(shape[-3:])))
    RESUME_BLOCK = (0, 0)
    last_save_lut_ind = RESUME_BLOCK[1]
    for indices in product(*input_indices):    
        if count % 100 == 0:
            print('Processing', count, '/', size)    
        count += 1

    # for sza, vza, raa, aod, band in product(*input_params):
    # for i in range(5):
        # sza, vza, raa, aod, band = random_product(*input_params)
        # sza, vza, raa, aod, band = 0.10, 0.20, 30, 0.1, 200+i
        sza, vza, raa, aod, band = [input_params[i][v] for i, v in enumerate(indices)]
        if indices[0] < RESUME_BLOCK[0] or (indices[0] == RESUME_BLOCK[0] and indices[1] < RESUME_BLOCK[1]):
            continue
                
        if indices[1] != last_save_lut_ind:
            last_save_lut_ind = indices[1]
            target_sza_ind = indices[0]
            if last_save_lut_ind == 0:
                target_sza_ind -= 1
                target_vza_ind = 15
            else: 
                target_vza_ind = last_save_lut_ind - 1
            
            if not args.no_save:    
                print('Saving block...', target_sza_ind, target_vza_ind)
                print(' ', np.count_nonzero(lut_block))
                with Dataset(nc_filepath, 'a') as nc:
                    lut = nc.variables['Lutvars']
                    lut[:, target_sza_ind, target_vza_ind, :, :, :] = lut_block
                    
                lut_block[:] = 0
                print('Saved')
        
        # output_path = output_dir / f"{count}_output_test.txt"
        # print(input_text)
        # thread = threading.Thread(target=run_fortran_executable, args=(executable_path, (sza, vza, raa, aod, band), output_path))
        
        # thread.start()
        run_fortran_executable(
            executable_path, 
            (sza, vza, raa, aod, band), 
            input_indices=indices, 
            output_mask=lut_block, 
            BLOCK=True,
            LOG=args.no_save
        )

    print('Done')
