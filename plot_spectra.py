#!/usr/bin/python

from spectrum import *
import matplotlib.pyplot as plt 
import logging
logging.basicConfig(filename='spyctrum.log',level=logging.DEBUG)

def main():
   logging.info('SPYCTRUM a program better than its name')
   escfout = "escf.out"
   refuvcsv = "refuv.csv"
   refcdcsv = "refcd.csv"
#
   logging.info( "Reading file {0}".format(escfout))
   wl, uv, cd = read_tm_spectrum(escfout)
   logging.info( "  found {0} wavelength".format(len(wl)))
   logging.info( "Initializition of Theoretical Spectrum")
   spectrumTh = Spectrum(wl=wl, uv=uv, cd=cd)
   logging.info( "  setting range ...")
   spectrumTh.setRange(200, 450)
   logging.info( "  computing spectrum ...")
   spectrumTh.compute_spectrum(gamma=200)
   x=spectrumTh.getLambdas()   
   uv_th=spectrumTh.getUV()   
   cd_th=spectrumTh.getCD()   
   logging.info( "Theoretical spectra computed between {0} and {1} at {2} values".format(min(x), max(x), len(x)))
   logging.info( "   UV spectrum: max {0} min {1} at {2} pts.".format(min(uv_th), max(uv_th), len(uv_th)))
   logging.info( "   CD spectrum: max {0} min {1} at {2} pts.".format(min(cd_th), max(cd_th), len(cd_th)))
#
   logging.info( "Reading file {0}".format(refuvcsv))
   wl, uv = read_csv_spectrum(refuvcsv)
   logging.info( "  found {0} wavelength".format(len(wl)))
   logging.info( "Reading file {0}".format(refcdcsv))
   alt_wl, cd = read_csv_spectrum(refcdcsv)
   logging.info( "  found {0} wavelength".format(len(alt_wl)))
   logging.info( "Initialization of Experimental Spectrum")
   spectrumExp = Spectrum(wl=wl, uv=uv, alt_wl=alt_wl, cd=cd)
   logging.info( "  setting range ...")
   spectrumExp.setRange(200, 450)
   logging.info( "  interpolating spectrum ...")
   spectrumExp.interpolate_spectrum()
   x=spectrumTh.getLambdas()   
   uv_exp=spectrumExp.getUV()
   cd_exp=spectrumExp.getCD()
   logging.info( "Experimental spectra interpolated between {0} and {1} at {2} values".format(min(x), max(x), len(x)))
   logging.info( "   UV spectrum: max {0} min {1} at {2} pts.".format(min(uv_exp), max(uv_exp), len(uv_exp)))
   logging.info( "   CD spectrum: max {0} min {1} at {2} pts.".format(min(cd_exp), max(cd_exp), len(cd_exp)))
#
   logging.info( "Plotting")
   fig, axes = plt.subplots(nrows=2, ncols=2)
   uv_plot_exp, = axes[0,0].plot(x, uv_exp, '-' , label="UV Exp")
   axes[0,0].legend(loc="lower right")
   axes[0,0].grid(True, which='both')
   axes[0,0].axhline(y=0, color='k')
   uv_plot_th,  = axes[1,0].plot(x, uv_th, '--', label="UV Th")
   axes[1,0].legend(loc="lower right")
   axes[1,0].grid(True, which='both')
   axes[1,0].axhline(y=0, color='k')
   cd_plot_exp, = axes[0,1].plot(x, cd_exp, '-' , label="CD Exp")
   axes[0,1].legend(loc="lower right")
   axes[0,1].grid(True, which='both')
   axes[0,1].axhline(y=0, color='k')
   cd_plot_th,  = axes[1,1].plot(x, cd_th, '--', label="CD Th")
   axes[1,1].legend(loc="lower right")
   axes[1,1].grid(True, which='both')
   axes[1,1].axhline(y=0, color='k')
   fig.tight_layout()
   plt.show()
#   plt.plot(x, cd_th, '--', x, cd_exp, '-' )
#   for i in range(len(x)):
#      logging.info( x[i], uv_th[i], uv_exp[i]

if __name__ == '__main__':
    main()
