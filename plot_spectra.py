#!/usr/bin/python

import argparse
from spectrum import *
import matplotlib.pyplot as plt 
import logging
import numpy as np
logging.basicConfig(filename='spyctrum.log',level=logging.DEBUG)

def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("-p", "--phase", help="switches the phase of the theoretical cd spectrum", action="store_true")
   parser.add_argument("-t", "--output", help="TURBOMOLE escf output", default="escf.out")
   parser.add_argument("-u", "--uv", help="UV data file", default="refuv.csv")
   parser.add_argument("-c", "--cd", help="CD data file", default="refcd.csv")
   parser.add_argument("-s", "--shift", help="shift value on the energies", type=float, default=1.0)
   parser.add_argument("-g", "--gamma", help="gamma value in eV", type=float, default=0.25)
   parser.add_argument("-r", "--gamma_range", help="gamma min max step values in eV", type=float, nargs=3, default=None)
   args = parser.parse_args()
#Default values
   phase=1
   MODE="single"
#
   shift=args.shift
   gamma=args.gamma
   gammaRange=args.gamma_range
   if args.phase:
      print "Phase argument toggled"
      phase=-1
   if gammaRange!=None:
      gammaRange=np.linspace(args.gamma_range[0],args.gamma_range[1],args.gamma_range[2])
      MODE="scanGamma"
   logging.info('SPYCTRUM a program better than its name')
   escfout = args.output
   refuvcsv = args.uv
   refcdcsv = args.cd
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
   logging.info( "Reading file {0}".format(escfout))
#
# Theoretical bloc
#
   wl, uv, cd = read_tm_spectrum(escfout)
   logging.info( "  found {0} wavelength".format(len(wl)))
   if MODE=="single":
      spectrumTh = Spectrum.SpectrumThfactory(wl, uv, cd, phase, 200, 450, gamma, shift)
   elif MODE=="scanGamma":
      spectrumTh = []
      for gamma in gammaRange:
         spectrumTh.append(SpectrumThfactory(wl, uv, cd, phase, 200, 450, gamma, shift))
#
   if MODE=="single":
      uv_th=spectrumTh.getUV()
      cd_th=spectrumTh.getCD()
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
