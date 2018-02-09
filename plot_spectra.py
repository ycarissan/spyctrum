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
   spectrumTh.compute_spectrum(200)
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
   cd_th=[-10000*i for i in cd_th]
   plt.plot(x, cd_th, '--', x, uv_exp, '-' )
   plt.show()
#   for i in range(len(x)):
#      print x[i], uv_th[i], uv_exp[i]

if __name__ == '__main__':
    main()
