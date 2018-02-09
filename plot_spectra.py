#!/usr/bin/python

import matplotlib.pyplot as plt 
from spectrum import *

def main():
   escfout = "escf.out"
   refcsv = "ref.csv"
#
   print "Reading ", escfout
   wl, uv, cd = read_tm_spectrum(escfout)
   print "Init Th Spectrum"
   spectrumTh = Spectrum(wl, uv, cd)
   print "  set range"
   spectrumTh.setRange(200, 450)
   print "  compute spectrum"
   spectrumTh.compute_spectrum()
   x=spectrumTh.getLambdas()   
   uv_th=spectrumTh.getUV()   
   cd_th=spectrumTh.getCD()   
#
   print "Reading ", refcsv
   wl, uv = read_csv_spectrum(refcsv)
   print "Init Exp Spectrum"
   spectrumExp = Spectrum(wl, uv)
   print "  set range"
   spectrumExp.setRange(200, 450)
   print "  interpolate spectrum"
   spectrumExp.interpolate_spectrum()
   uv_exp=spectrumExp.getUV()
#
   print "Plotting"
   plt.plot(x, uv_th, 'o', x, uv_exp, '-' )
   plt.show()

if __name__ == '__main__':
    main()
