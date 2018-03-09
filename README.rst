============
Spyctrum
============
Tool to generate uv and/or cd spectra from a TURBOMOLE calculation.
A reference spectrum can be provided and the program tries to fit the spectra.

***************
usage
***************

usage: spyctrum.py [-h] [-p] [-t OUTPUT] [-u UV] [-c CD] [-s SHIFT] [-g GAMMA]
                   [-r GAMMA_RANGE GAMMA_RANGE GAMMA_RANGE]
                   [-v SHIFT_RANGE SHIFT_RANGE SHIFT_RANGE] [-m MODE]

optional arguments:
  -h, --help            show this help message and exit
  -p, --phase           switches the phase of the theoretical cd spectrum
  -t OUTPUT, --output OUTPUT
                        TURBOMOLE escf output
  -u UV, --uv UV        UV data file
  -c CD, --cd CD        CD data file
  -s SHIFT, --shift SHIFT
                        shift value on the energies
  -g GAMMA, --gamma GAMMA
                        gamma value in eV
  -r GAMMA_RANGE GAMMA_RANGE GAMMA_RANGE, --gamma_range GAMMA_RANGE GAMMA_RANGE GAMMA_RANGE
                        gamma min max nstep values in eV
  -v SHIFT_RANGE SHIFT_RANGE SHIFT_RANGE, --shift_range SHIFT_RANGE SHIFT_RANGE SHIFT_RANGE
                        shift min max nstep values in eV
  -m MODE, --mode MODE  MODE single|table|convolution

***************
examples
***************

To get the convoluted spectrum from a turbomole output in a file named convolution.csv:

``#spyctrum -t escf.log -m convolution``

To get the original spectrum from a turbomole output in a file named table.csv:

``#spyctrum -t escf.log -m table``

To plot the UV spectrum with gnuplot:

``gnuplot``

``> plot 'convolution.csv' u 1:2 w l, 'table.csv' u 1:2 w i``

To plot the CD spectrum with gnuplot:

``gnuplot``

``> plot 'convolution.csv' u 1:3 w l, 'table.csv' u 1:3 w i``

