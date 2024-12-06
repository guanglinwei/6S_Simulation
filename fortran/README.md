# 6S LUT Generation
## Important Files
- `input6S_plt.in`: where parameters are input, like SZA, VZA, etc...
- `paramdef.inc`: no completely sure, but looks like more parameters

## Instructions
Note that these instructions are for a Linux environment.

### 6S
Install the 6S code [here](https://salsa.umd.edu/6spage.html) and extract it. Open a command prompt in the root directory of the extracted 6S project.

### Fortran
Install Fortran by follow [these instructions](https://fortran-lang.org/en/learn/os_setup/install_gfortran/). For example, on Linux, do:
- `sudo apt install gfortran`

### Build Executable
Install make, then make the executable:
- `sudo apt-get install build-essential`
- `make`

### Run Executable
- `./sixsV2.1 < input6S_plf.in > 6s_out.txt`

The above filenames can be replaced as necessary.

## Issues and Fixes
The following two lines was added to the Makefile to account for newer Fortran versions:
```
EXTRA	= -std=legacy
EXTRA	= -ffixed-line-length-none
```