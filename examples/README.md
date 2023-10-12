# qfmu

[qfmu](https://github.com/hyumo/qFMU) is a python package to generate `continuous-time`, `LTI` system FMUs from command line. 

## FMU Export compatibility Info

- All example FMUs have been exported by `qFMU` (see [build.py](scripts/build.py))
- All example FMUs contain multi-platform binaries (`win64`, `linux64`, `darwin64`)
- All example FMUs are free to be shared for cross-check purposes

| model           	| win64 	| linux64 	| darwin64 	|
|-----------------	|-------	|---------	|----------	|
| FirstOrder.fmu  	| ME,CS 	| ME,CS   	| ME,CS    	|
| SecondOrder.fmu 	| ME,CS 	| ME,CS   	| ME,CS    	|
| SISO.fmu        	| ME,CS 	| ME,CS   	| ME,CS    	|
| MIMO.fmu        	| ME,CS 	| ME,CS   	| ME,CS    	|

### Validation Info

Validation tools

- FMPy 0.3.16