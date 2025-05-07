# Converts SRF text files into .f code

import argparse
import os
import numpy as np

MIN_WV = 0.25
WV_INTERVAL = 0.0025
WV_INCREMENT_COUNT = 1501

def parse_srf(filepath):
    wavelengths = []
    srfs = []

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            parts = line.split()
            if len(parts) >= 3:
                wavelengths.append(float(parts[0]))
                srfs.append(float(parts[2]))

    return wavelengths, srfs

def lerp(orig_min, orig_max, value, new_min, new_max):
    """
    Linearly interpolates a value from the original range to a new range.

    Args:
        orig_min (float): Minimum of the original range.
        orig_max (float): Maximum of the original range.
        value (float): Value within the original range.
        new_min (float): Minimum of the new range.
        new_max (float): Maximum of the new range.

    Returns:
        float: Interpolated value in the new range.
    """
    if orig_max == orig_min:
        raise ValueError("Original range must not be zero.")
    return new_min + (value - orig_min) * (new_max - new_min) / (orig_max - orig_min)

def format_f_filename(filename):
    f_name, ext = os.path.splitext(filename)
    f_name = str(f_name).lower()
    return f'{f_name.upper()}{ext}', f_name, ext

def resample_srf(wavelengths, srfs):
    '''
    6S requires SRF values to be given for each wavelength value from 0.25um to 4um with 0.0025um (0.25nm) increments, 
    totaling 1501 entries. Wavelengths in the provided SRFs are not necessarily in increments of 0.0025um. This function 
    resamples from the SRFs to match up with the required increment size.
    '''
    if len(wavelengths) != len(srfs):
        raise ValueError(f'wavelengths and srfs are different lengths: {len(wavelengths)} != {len(srfs)}')
    
    # TODO: should also ensure wavelengths are sorted
    
    fixed_wavelengths = np.linspace(MIN_WV, MIN_WV + WV_INTERVAL * (WV_INCREMENT_COUNT - 1), WV_INCREMENT_COUNT)
    
    curr_wv_index = 0
    input_wv_index = 0
    resampled_srfs = []
    input_wv_count = len(wavelengths)
    left_pad = -1 # number of zeros before first non-zero value
    right_pad = -1 # number of zeros after last non-zero value
    
    while curr_wv_index < WV_INCREMENT_COUNT:
        target_wv = fixed_wavelengths[curr_wv_index] # wavelength we need to find SRF for
        if target_wv < wavelengths[0]:
            curr_wv_index += 1
            continue
            
        if left_pad == -1:
            left_pad = curr_wv_index
        
        while input_wv_index < input_wv_count and wavelengths[input_wv_index] < target_wv:
            input_wv_index += 1
        # print(input_wv_index)
        # print(wavelengths[input_wv_index], input_wv_index, target_wv, curr_wv_index)
        if input_wv_index == input_wv_count:
            resampled_srfs.append(0)
            break
            
        resampled_srf = lerp(
            wavelengths[input_wv_index - 1], wavelengths[input_wv_index], 
            target_wv.item(), 
            srfs[input_wv_index - 1], srfs[input_wv_index]
        )
        
        resampled_srfs.append(resampled_srf)
        curr_wv_index += 1
        
    right_pad = WV_INCREMENT_COUNT - len(resampled_srfs) - left_pad
    
    return left_pad, right_pad, resampled_srfs

def output_f_file(left_pad, right_pad, resampled_srfs, filename, comment=None, output_dir='./fortran/'):
    out_name, f_name, ext = format_f_filename(filename)
    band_count = 1 # TODO: multiple bands in same file
    
    if not os.path.exists(output_dir):
        print('Making directory', output_dir)
        os.mkdir(output_dir)
    
    with open(os.path.join(output_dir, out_name), 'w') as f_out:
        # Header
        f_out.write(f'      subroutine {f_name}(iwa)\n' + \
                    f'      common /sixs_ffu/ s({WV_INCREMENT_COUNT}),wlinf,wlsup\n' + \
                    f'      real sr({band_count},{WV_INCREMENT_COUNT}),wli({band_count}),wls({band_count})\n' + \
                    f'      real s,wlinf,wlsup\n' + \
                    f'      integer iwa,l,i\n')
        
        # Comment
        f_out.write(f'c\n' + \
                   (f'c    {comment}\n' if comment is not None else '') + \
                    f'c\n')
        
        # SRF Table
        f_out.write((' ' * 6) + f'data (sr(1,l),l=1,{WV_INCREMENT_COUNT})/  {left_pad}*0,\n')
        srfs_per_line = 7
        for i in range(0, len(resampled_srfs), srfs_per_line):
            to_add = resampled_srfs[i:min((i+srfs_per_line), len(resampled_srfs))]
            to_write = []
            for value in to_add:
                if value < 1.0:
                    to_write.append(f' {value:.8f},'.lstrip('0'))
                else:
                    to_write.append(f'{value:.8f},')
                
            f_out.write((' ' * 5) + 'a' + (''.join(to_write)) + '\n')
            
        f_out.write((' ' * 5) + f'a{right_pad}*0./\n')
        
        # Outputs
        f_out.write(
            f'      wli({1})={(0.25 + 0.0025 * left_pad + 0.00001):0.4f}\n' + \
            f'      wls({1})={(0.25 + 0.0025 * (left_pad + len(resampled_srfs)) - 0.0001):0.6f}\n' + \
             '      do 1 i=1,1501\n      s(i)=sr(iwa,i)\n' + \
             '    1 continue\n      wlinf=wli(iwa)\n      wlsup=wls(iwa)\n' + \
             '      return\n      end\n\n'
        )
        
def convert_all_srf_to_f(input_files, output_filenames, out_dir):
    for input_file, output_file in zip(input_files, output_filenames):
        wavelengths, srfs = parse_srf(input_file)
        left_pad, right_pad, resampled_srfs = resample_srf(wavelengths, srfs)
        
        output_f_file(left_pad, right_pad, resampled_srfs, output_file, 
                      comment=f'Generated from {os.path.basename(input_file)}',
                      output_dir=out_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert SRF text files to Fortran code.")
    parser.add_argument(
        '-i', '--input-files',
        dest="input_files", 
        nargs="+", 
        required=False,
        help="Paths to input SRF text files."
    )
    parser.add_argument(
        '-r', '--recursive',
        dest='recursive_dir',
        nargs='?',
        const='./srf/', 
        type=str,       
        help='Directory to read Fortran files from.'
    )
    parser.add_argument(
        '-o', '--output-files',
        dest="output_files", 
        nargs="+", 
        required=True,
        help="Names of output Fortran files."
    )
    parser.add_argument(
        '-e', '--override',
        dest='override',
        default=False,
        action='store_true',
        help='Override existing .f files with output. Not recommended.'
    )
    parser.add_argument(
        '-d', '--out-dir',
        dest='out_dir',
        default='./f_out/',
        help='Directory to output Fortran files. Defaults to "./f_out/"'
    )
    # parser.add_argument(
    #     '-e', '--edit-6s',
    #     dest='edit_sixs',
    #     default=False,
    #     action='store_true',
    #     help='Edit the Makefile and main.f of the 6S code to include the newly generated .f file.'
    # )

    args = parser.parse_args()

    if not args.input_files and not args.recursive_dir:
        parser.error('Must either provide separate input files with -i <input_files> or a directory with -r <directory>. Use -h for more info.')
    
    if args.input_files and args.recursive_dir:
        print('Both file list and directory are provided. Ignoring the directory and only using provided input files.')
    
    input_files = []
    if args.input_files:
        input_files = args.input_files
    else:
        for filename in os.scandir(args.recursive_dir):
            if filename.is_file():
                input_files.append(filename.path)
      
    # Ensure equal number of input and output files
    if len(input_files) != len(args.output_files):
        raise ValueError("Number of input files must equal number of output files.")
    
    # if not os.path.isdir(args.out_dir):
        # parser.error(f'{args.out_dir} is not a directory.')

    for in_file in input_files:
        if not os.path.exists(in_file) or not os.path.isfile(in_file):
            parser.error(f'{in_file} does not exist or is not a file.')
    
    output_files = []
    for out_file in args.output_files:
        ext = os.path.splitext(out_file)[1]
        if ext == '':
            out_file += '.f'
        elif ext != '.f':
            parser.error(f'{out_file} is not a valid fortran file. Must end with ".f".')
            
        out_name, _, _ = format_f_filename(out_file)
        if os.path.exists(os.path.join(args.out_dir, out_name)) and not args.override:
            parser.error(f'{os.path.join(args.out_dir, out_name)} already exists. Please use the --override flag to write over the existing file.')
            
        output_files.append(out_file)
    convert_all_srf_to_f(input_files, output_files, args.out_dir)