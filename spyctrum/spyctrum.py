#!/usr/bin/python

"""
Main module
"""
import argparse
import datetime
from spectrum import *
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt 
import logging
import numpy as np
logging.basicConfig(filename='spyctrum.log',level=logging.DEBUG)

def main():
   """
   Main routine
   """
   parser = argparse.ArgumentParser()
   parser.add_argument("-p", "--phase", help="switches the phase of the theoretical cd spectrum", action="store_true")
   parser.add_argument("-t", "--output", help="TURBOMOLE escf output", default="escf.out")
   parser.add_argument("-u", "--uv", help="UV data file", default="refuv.csv")
   parser.add_argument("-c", "--cd", help="CD data file", default="refcd.csv")
   parser.add_argument("-s", "--shift", help="shift value on the energies", type=float, default=1.0)
   parser.add_argument("-g", "--gamma", help="gamma value in eV", type=float, default=0.25)
   parser.add_argument("-r", "--gamma_range", help="gamma min max nstep values in eV", type=float, nargs=3, default=None)
   parser.add_argument("-v", "--shift_range", help="shift min max nstep values in eV", type=float, nargs=3, default=None)
   parser.add_argument("-m", "--mode", help="MODE single|table|convolution", default="single")
   args = parser.parse_args()
#Default values
   phase=1
   MODE=args.mode
#
   shift=args.shift
   gamma=args.gamma
   gammaRange=args.gamma_range
   shiftRange=args.shift_range
   if args.phase:
      print("Phase argument toggled")
      phase=-1
   if gammaRange!=None:
      gammaRange=np.linspace(args.gamma_range[0], args.gamma_range[1], args.gamma_range[2])
      MODE="scanGamma"
   if shiftRange!=None:
      shiftRange=np.linspace(args.shift_range[0], args.shift_range[1], args.shift_range[2])
      if MODE=="scanGamma":
         MODE="scanGamma scanShift"
      else:
         MODE="scanShift"
   logging.info('SPYCTRUM a program better than its name')
   logging.info('MODE : '+MODE)
   escfout = args.output
   refuvcsv = args.uv
   refcdcsv = args.cd
#
# Experimental bloc
#
   if ( not ( "table" in MODE or "convolution" in MODE ) ):
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
   if "single" in MODE or "table" in MODE or "convolution" in MODE:
      spectrumTh = Spectrum.SpectrumThfactory(wl, uv, cd, phase, 0, 4000, gamma, shift)
   elif "scanGamma" in MODE:
      spectrumTh = []
      for gamma in gammaRange:
         if "scanShift" in MODE:
            for shift in shiftRange:
               spectrumTh.append(Spectrum.SpectrumThfactory(wl, uv, cd, phase, 200, 450, gamma, shift))
         else:
            spectrumTh.append(Spectrum.SpectrumThfactory(wl, uv, cd, phase, 200, 450, gamma, shift))
      logging.info( "  {0} spectra generated".format(len(spectrumTh)))
#
   if "single" in MODE:
      x_th=spectrumTh.getLambdas()
      uv_th=spectrumTh.getUV()
      cd_th=spectrumTh.getCD()
      lambdas=spectrumTh.getWL_orig()
      uv_orig=spectrumTh.getUV_orig()
      cd_orig=spectrumTh.getCD_orig_phase()
      logging.info( "Plotting")
      fig, (axUV, axCD) = plt.subplots(ncols=1,nrows=2)
#UV bloc
      legUV = axUV.plot(x, uv_exp, '-', label="UV Exp")
      axUV2 = axUV.twinx()
      legUV2 = axUV2.plot(x_th, uv_th, '--', label="UV Th")
      axUV2.set_xlim(left=min(x), right=max(x))
      axUV2.stem(lambdas, uv_orig, '-', markerfmt=".", label="UV values")
      leg=legUV+legUV2
      lbl=[l.get_label() for l in leg]
      axUV.legend(leg, lbl, loc="upper right")
      axUV.grid(True, which="both")
#CD bloc
      legCD = axCD.plot(x, cd_exp, '-' , label="CD Exp")
      axCD2 = axCD.twinx()
      legCD2 = axCD2.plot(x_th, cd_th, '--', label="CD Th")
      leg=legCD+legCD2
      lbl=[l.get_label() for l in leg]
      axCD2.legend(leg, lbl, loc="upper right")
      axCD.grid(True, which="both")
      axCD.axhline(y=0, color='k')
#
      plt.show()
   elif "table" in MODE:
      fid = open("table.csv","w")
      lambdas=spectrumTh.getWL_orig()
      uv_orig=spectrumTh.getUV_orig()
      cd_orig=spectrumTh.getCD_orig_phase()
      fid.write("#Th spectrum (original)\n")
      for i in range(len(lambdas)):
         fid.write("{0} {1} {2}\n".format(lambdas[i], uv_orig[i], cd_orig[i]))
   elif "convolution" in MODE:
      fid = open("convolution.csv","w")
      x_th=spectrumTh.getLambdas()
      uv_th=spectrumTh.getUV()
      cd_th=spectrumTh.getCD()
      fid.write("#Th spectrum (convoluted)\n")
      for i in range(len(x_th)):
         fid.write("{0} {1} {2}\n".format(x_th[i], uv_th[i], cd_th[i]))
   elif "scanGamma" in MODE or "scanShift" in MODE:
      with PdfPages('spyctrum_pdf.pdf') as pdf:
         for sp in spectrumTh:
            x_th=sp.getLambdas()
            uv_th=sp.getUV()
            cd_th=sp.getCD()
            lambdas=sp.getWL_orig()
            uv_orig=sp.getUV_orig()
            cd_orig=sp.getCD_orig_phase()
            logging.info("Plotting Gamma={0} Shift={1} Phase={2}".format(sp.getGamma(), sp.getShift(), sp.getPhase()))
            fig, (axUV, axCD) = plt.subplots(ncols=1,nrows=2)
#UV bloc
            legUV = axUV.plot(x, uv_exp, '-', label="UV Exp")
            axUV2 = axUV.twinx()
            legUV2 = axUV2.plot(x_th, uv_th, '--', label="UV Th")
#            axUV3 = axUV.twinx()
#            axUV3 = axUV.twiny()
#            axUV3.tick_params( axis='y', which='both', left='off', right='off', labelright='off')
            axUV.set_xlim(left=min(x), right=max(x))
            axUV2.set_xlim(left=min(x), right=max(x))
            axUV2.stem(lambdas, uv_orig, '-', markerfmt=".", label="UV values")
            leg=legUV+legUV2
            lbl=[l.get_label() for l in leg]
            axUV.legend(leg, lbl, loc="upper right")
            axUV.grid(True, which="both")
#CD bloc
            legCD = axCD.plot(x, cd_exp, '-' , label="CD Exp")
            axCD2 = axCD.twinx()
            legCD2 = axCD2.plot(x_th, cd_th, '--', label="CD Th")
#            axCD3 = axCD.twinx()
#            axCD3 = axCD.twiny()
#            axCD3.tick_params( axis='y', which='both', left='off', right='off', labelright='off')
#            stemscale=0.9*max([abs(a) for a in cd_th])/max([abs(a) for a in cd_orig])
#            axCD2.stem(lambdas, [a/stemscale for a in cd_orig], '-', markerfmt=".", label="CD values")
            axCD.set_xlim(left=min(x), right=max(x))
            axCD.set_ylim(bottom=-400, top= 400, auto=False)
            axCD2.set_ylim(bottom=-0.12, top= 0.12, auto=False)
            axCD2.stem(lambdas, cd_orig, '-', markerfmt=".", label="CD values")
            leg=legCD+legCD2
            lbl=[l.get_label() for l in leg]
            axCD.legend(leg, lbl, loc="upper right")
            axCD.grid(True, which="both")
            axCD.axhline(y=0, color='k')
            plt.title("Gamma={0} Shift={1} Phase={2}".format(sp.getGamma(), sp.getShift(), sp.getPhase()))
            pdf.savefig(fig)  # saves the current figure into a pdf page
            plt.close()
         # We can also set the file's metadata via the PdfPages object:
         d = pdf.infodict()
         d['Title'] = 'Multipage PDF scan over gamma values'
         d['Author'] = 'auto'
         d['Subject'] = 'Scan over gamma values'
         d['Keywords'] = 'scan gamma UV CD'
         d['ModDate'] = datetime.datetime.today()

if __name__ == '__main__':
    main()
