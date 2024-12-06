# 6S LUT Generation
## Instructions
Note that these instructions are for a Linux environment. Please install WSL if you are running Windows.

### 6S
Install the 6S code [here](https://salsa.umd.edu/6spage.html) and extract it. Open a command prompt in the root directory of the extracted 6S project.

### Fortran
Install Fortran by follow [these instructions](https://fortran-lang.org/en/learn/os_setup/install_gfortran/). For example, on Linux, do:
- `sudo apt install gfortran`

### Build Executable
Install make, then make the executable in `/fortran/`:
- `sudo apt-get install build-essential`
- `cd fortran`
- `make`
- `make sixs`
- `cd ..`

### Python Setup
- Install `pip`
- `python3 -m pip intall virtualenv`
- `python3 -m venv .venv`
- `. .venv/bin/activate`
- `python3 -m pip install -r requirements.txt`

### Run Python Script
- `python3 run.py`

## Notes
Line ~1400: put the subroutine names here