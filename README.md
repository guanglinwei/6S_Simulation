# 6S LUT Generation
This project generates a lookup table with Radiative Transfer simulations using [6S code](https://salsa.umd.edu/6spage.html).

## Setup
### Platform
This code is intended for a Linux environment. If you are running Windows, please [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

### Fortran
If you are on Linux:
- `sudo apt install gfortran`

Otherwise, follow [these instructions](https://fortran-lang.org/en/learn/os_setup/install_gfortran/). 

### Python Virtual Environment
- Ensure you have python3 and pip installed
- `python3 -m pip install virtualenv`
- `python3 -m venv .venv`
- `. .venv/bin/activate`
- `python -m pip install -r requirements.txt`

## Simulation Preparation
### SRF to Fortran Conversion
Converts a spectral response function text file to a Fortran program.

`python srf_txt_to_fortran.py -i [INPUT_FILES] -o [OUTPUT_FILES]`
- `INPUT_FILES`: paths to the SRF text files. Ex: `-i srf/GOES-R_ABI_PFM_SRF_CWG_ch1.txt srf/GOES-R_ABI_PFM_SRF_CWG_ch2.txt`
- `OUTPUT_FILES`: names of output files. Ex: `-o goesr1.f goesr2.f`

Outputs default to the `f_out` directory.

Run `python srf_txt_to_fortran.py -h` to see more options.

### Add Fortran Code to Simulation
Creates the modified 6S code. By default, outputs to `fortran` directory.

`python edit_6s_code.py -o -r`
- Defaults to reading from the `f_out` directory for SRFs and the `base_fortran` directory for 6S code. 

Run `python edit_6s_code.py -h` to see more options.

## Creating the Lookup Table
`python run.py --make`

This will compile the 6S code and create the lookup table in blocks.
Run without the `--make` option if you have already compiled the 6S executable. 

Run `python run.py -h` to see more options.