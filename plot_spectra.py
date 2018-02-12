#!/usr/bin/python

import argparse
from spectrum import *
import matplotlib.pyplot as plt 
import logging
logging.basicConfig(filename='spyctrum.log',level=logging.DEBUG)

def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("-p", "--phase", help="switches the phase of the theoretical cd spectrum", action="store_true")
   args = parser.parse_args()
   if args.phase:
      print "Phase argument toggled"
      phase=-1
   logging.info('SPYCTRUM a program better than its name')
   escfout = "escf.out"
   refuvcsv = "refuv.csv"
   refcdcsv = "refcd.csv"
#
# Experimental bloc
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
   x=spectrumExp.getLambdas()
   uv_exp=spectrumExp.getUV()
   cd_exp=spectrumExp.getCD()
   logging.info( "Experimental spectra interpolated between {0} and {1} at {2} values".format(min(x), max(x), len(x)))
   logging.info( "   UV spectrum: max {0} min {1} at {2} pts.".format(min(uv_exp), max(uv_exp), len(uv_exp)))
   logging.info( "   CD spectrum: max {0} min {1} at {2} pts.".format(min(cd_exp), max(cd_exp), len(cd_exp)))
#
# Theoretical bloc
#
   logging.info( "Reading file {0}".format(escfout))
   wl, uv, cd = read_tm_spectrum(escfout)
   logging.info( "  found {0} wavelength".format(len(wl)))
   logging.info( "Initialization of Theoretical Spectrum")
   spectrumTh = Spectrum(wl=wl, uv=uv, cd=cd, phase=phase)
   logging.info( "  setting range ...")
   spectrumTh.setRange(200, 450)
   logging.info( "  computing spectrum ...")
   spectrumTh.compute_spectrum(gamma=0.20, shift=1.00)
   x=spectrumTh.getLambdas()   
   uv_th=spectrumTh.getUV()   
   cd_th=spectrumTh.getCD()   
   logging.info( "Theoretical spectra computed between {0} and {1} at {2} values".format(min(x), max(x), len(x)))
   logging.info( "   UV spectrum: max {0} min {1} at {2} pts.".format(min(uv_th), max(uv_th), len(uv_th)))
   logging.info( "   CD spectrum: max {0} min {1} at {2} pts.".format(min(cd_th), max(cd_th), len(cd_th)))
#
   logging.info( "Plotting")
   fig, (axUV, axCD) = plt.subplots(ncols=1,nrows=2)
#UV bloc
   legUV = axUV.plot(x, uv_exp, '-', label="UV Exp")
   axUV2 = axUV.twinx()
   legUV2 = axUV2.plot(x, uv_th, '--', label="UV Th")
   leg=legUV+legUV2
   lbl=[l.get_label() for l in leg]
   axUV.legend(leg, lbl, loc="upper right")
   axUV.grid(True, which="both")
#CD bloc
   legCD = axCD.plot(x, cd_exp, '-' , label="CD Exp")
   axCD2 = axCD.twinx()
   legCD2 = axCD2.plot(x, cd_th, '--', label="CD Th")
   leg=legCD+legCD2
   lbl=[l.get_label() for l in leg]
   axCD2.legend(leg, lbl, loc="upper right")
   axCD.grid(True, which="both")
   axCD.axhline(y=0, color='k')
#
   plt.show()

if __name__ == '__main__':
    main()
