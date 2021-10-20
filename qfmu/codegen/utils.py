


import sys
import warnings

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
    