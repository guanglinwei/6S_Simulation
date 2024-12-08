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

`python srf_txt_to_fortran.py -r srf -o goesr1 goesr2 goesr3 goesr5 goesr6`
- `-r [INPUT_DIRECTORY]`: directory to read SRF files from.
- `-o [OUTPUT_FILES]`: names of output files. Must have same number of entries as files in input directory.

Outputs default to the `f_out` directory.

Run `python srf_txt_to_fortran.py -h` to see more options.

If you would like to convert SRFs in code:
```python
from srf_txt_to_fortran import convert_all_srf_to_f

convert_all_srf_to_f(['srf1.txt', 'srf2.txt'], ['out1', 'out2'], './f_out')
```

### Add Fortran Code to Simulation
Creates the modified 6S code. By default, outputs to `fortran` directory.

`python edit_6s_code.py -e -r`
- Defaults to reading from the `f_out` directory for SRFs and the `base_fortran` directory for 6S code. 

Run `python edit_6s_code.py -h` to see more options.

## Creating the Lookup Table
`python run.py --make`

This will compile the 6S code and create the lookup table in blocks.
Run without the `--make` option if you have already compiled the 6S executable. 

Run `python run.py -h` to see more options.