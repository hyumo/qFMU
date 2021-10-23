

import ast
from typing import List
import numpy as np

import sys
import warnings

def str_to_1d_array(data: str)->np.ndarray:
    # Replace [] with empty
    for char in '[]':
        data = data.replace(char, '')
    
    # Replace multiple spaces with single space
    while '  ' in data:
        data = data.replace('  ', ' ')
    
    # Remove the trailing ;
    if data.endswith(';'):
        data = data[:-1]
    elif data.endswith('; '):
        data = data[:-2]
        
    # 1D array
    if ';' not in data:
        if ',' in data:
            return np.fromstring(data, dtype=float, sep=',')
        else:        
            return np.fromstring(data, dtype=float, sep=' ')
    elif data.count(';') == 1 and data.endswith(';'):
        return np.fromstring(data, dtype=float, sep=' ')
    else:
        raise ValueError("Invalid vector format.")

def str_to_2d_array(data:str)->np.ndarray:
    if ";" not in data:
        raise ValueError("Invalid matrix format. Rows should be separated by ;")
    # Replace [] with empty
    for char in '[]':
        data = data.replace(char, '')
    # Replace multiple spaces with single space
    while '  ' in data:
        data = data.replace('  ', ' ')
    
    # 2D array
    rows = data.split(';')
    arr = []
    count = 0
    for row in rows:
        newrow = str_to_1d_array(row)
        if count == 0:
            ncols = newrow.shape[0]
        elif newrow.shape[0] != ncols:
            raise ValueError("Invalid matrix format. Each row should have the same number of values.")
        count += 1
        arr.append(newrow)
    return np.asarray(arr)


def fmi_platform():
    """determine fmi platform 
        
        - win32/64
        - linux32/64
        - darwin32/64

    Raises:
        Exception: [description]
    """
    if sys.platform.startswith('win'):
        platform = 'win'
    elif sys.platform.startswith('linux'):
        platform = 'linux'
    elif sys.platform.startswith('darwin'):
        warnings.warn("qfmu has not been tested on Macs, becuase I don't have one. Use it with caution.")
        platform = 'darwin'
    else:
        raise Exception("Unsupported platform: " + sys.platform)

    if sys.maxsize > 2**32:
        platform += '64'
    else:
        platform += '32'
    
    return platform