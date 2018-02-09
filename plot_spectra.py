#!/usr/bin/python

from spectrum import *
import matplotlib.pyplot as plt 
import logging
logging.basicConfig(filename='spyctrum.log',level=logging.DEBUG)

def main():
   logging.info('SPYCTRUM a program better than its name')
   escfout = "escf.out"
   refcsv = "ref.csv"
#
   print "Reading file ", escfout
   wl, uv, cd = read_tm_spectrum(escfout)
   print "  found {0} wavelength".format(len(wl))
   print "Initializition of Theoretical Spectrum"
   spectrumTh = Spectrum(wl, uv, cd)
   print "  setting range ..."
   spectrumTh.setRange(200, 450)
   print "  computing spectrum ..."
   spectrumTh.compute_spectrum(gamma=200)
   x=spectrumTh.getLambdas()   
   uv_th=spectrumTh.getUV()   
   cd_th=spectrumTh.getCD()   
   print "Theoretical spectra computed between {0} and {1} at {2} values".format(min(x), max(x), len(x))
   print "   UV spectrum: max {0} min {1} at {2} pts.".format(min(uv_th), max(uv_th), len(uv_th))
   print "   CD spectrum: max {0} min {1} at {2} pts.".format(min(cd_th), max(cd_th), len(cd_th))
#
   print "Reading file ", refcsv
   wl, uv, cd = read_csv_spectrum(refcsv)
   print "  found {0} wavelength".format(len(wl))
   print "Initialization of Experimental Spectrum"
   spectrumExp = Spectrum(wl, uv, cd)
   print "  setting range ..."
   spectrumExp.setRange(200, 450)
   print "  interpolating spectrum ..."
   spectrumExp.interpolate_spectrum()
   x=spectrumTh.getLambdas()   
   uv_exp=spectrumExp.getUV()
   cd_exp=spectrumExp.getCD()
   print "Experimental spectra interpolated between {0} and {1} at {2} values".format(min(x), max(x), len(x))
   print "   UV spectrum: max {0} min {1} at {2} pts.".format(min(uv_exp), max(uv_exp), len(uv_exp))
   print "   CD spectrum: max {0} min {1} at {2} pts.".format(min(cd_exp), max(cd_exp), len(cd_exp))
#
   print "Plotting"
   plt.plot(x, uv_th, '--', x, uv_exp, '-' )
   plt.plot(x, cd_th, '--', x, cd_exp, '-' )
   plt.show()
#   for i in range(len(x)):
#      print x[i], uv_th[i], uv_exp[i]

if __name__ == '__main__':
    main()
