#!/usr/bin/python

import matplotlib.pyplot as plt 
import spectrum

def main():
   escfout = "escf.out"
   refcsv = "ref.csv"
#
   npts=1000
   spectrumTh = SpectrumTheoretical(escfout)
   spectrumTh.generate_spectrum(npts)
#
   spectrumExp = SpectrumExperimental(refcsv)
   spectrumExp.generate_spectrum(npts)
#
   plt.plot(x, uv, 'o', xnew, ynew, '-' )
   plt.show()

   for x in spectrumTh.getLambda():
      print "{0:16.8f}\t{1:16.8f}\t{2:16.8f}".format(x, spectrumTh.getValue("uv",x), spectrumTh.getValue("cd",x))

if __name__ == '__main__':
    main()
