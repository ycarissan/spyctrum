#!/usr/bin/python

import re
import math
import numpy as np
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d
import logging
from scipy import constants

LOGRADICAL="  @class spectrum "

class Spectrum:
   """The Spectrum class handles uv/cd spectra.
   The class is initialized by values from computed or experimental values.
   Once initialized, the spectrum value can be obtained for any wavelength value.
   If the required wavelength is outside the initial boundaries the interpolated value
   is not reliable."""
   def __init__(self, wl=None, uv=None, alt_wl=None, cd=None, phase=1):
      logging.info("{0} {1}".format(LOGRADICAL, 'A new spectrum is created'))
      if wl==None:
         self.wl_orig=[]
      else:
         self.wl_orig=wl
      if uv==None:
         self.uv_orig=[]
      else:
         self.uv_orig=uv
      if alt_wl==None:
         self.alt_wl_orig=[]
      else:
         self.alt_wl_orig=alt_wl
      if cd==None:
         self.cd_orig=[]
      else:
         self.cd_orig=cd
      self.wl=[]
      self.uv=[]
      self.cd=[]
      self.gamma=float('nan')
      self.shift=float('nan')
      self.phase=phase

   def getShift(self):
      return self.shift

   def getGamma(self):
      return self.gamma

   def getPhase(self):
      return self.phase

   def getWL_orig(self):
      return self.wl_orig

   def getUV_orig(self):
      return self.uv_orig

   def getCD_orig(self):
      return self.cd_orig

   def getCD_orig_phase(self):
      return [a*self.phase for a in self.cd_orig]

   def setRange(self, xmin, xmax, npts=1000):
      if (xmin<min(self.wl_orig)):
         logging.info("Low wavelength value {0} lower than value allowed by uv spectrum {1}".format(xmin, min(self.wl_orig)))
         xmin=min(self.wl_orig)
      if len(self.alt_wl_orig)>0:
         if (xmin<min(self.alt_wl_orig)):
            logging.info("Low wavelength value {0} lower than value allowed by cd spectrum {1}".format(xmin, min(self.alt_wl_orig)))
            xmin=min(self.alt_wl_orig)
      if (xmax>max(self.wl_orig)):
         logging.info("High wavelength value {0} higher than value allowed by uv spectrum {1}".format(xmax, max(self.wl_orig)))
         xmax=max(self.wl_orig)
      if len(self.alt_wl_orig)>0:
         if (xmax>max(self.alt_wl_orig)):
            logging.info("High wavelength value {0} higher than value allowed by cd spectrum {1}".format(xmax, max(self.alt_wl_orig)))
            xmax=max(self.alt_wl_orig)
      self.wl   = np.linspace(xmin, xmax, npts)

   def interpolate_spectrum(self):
      """Interpolate the spectrum over the whole range of wavelength with cubic splines"""
      spectrum_interpolate_UV = interp1d(self.wl_orig, self.uv_orig, kind='cubic')
      self.uv   = spectrum_interpolate_UV(self.wl)
      if len(self.cd_orig)>0:
         if len(self.alt_wl_orig)!=0:
            spectrum_interpolate_CD = interp1d(self.alt_wl_orig, self.cd_orig, kind='cubic')
            self.cd   = spectrum_interpolate_CD(self.wl)
         else:
            spectrum_interpolate_CD = interp1d(self.wl_orig, self.cd_orig, kind='cubic')
            self.cd   = spectrum_interpolate_CD(self.wl)

   def compute_spectrum(self, gamma=10, shift=1):
      """Compute the values of a theoretical spectrum with fwhw=gamma
Gamma is applied on the energies in eV."""
      uv=[]
      cd=[]
      self.gamma=gamma
      self.shift=shift
      for i in range(len(self.wl)):
         uv.append(0)
         cd.append(0)
         x=self.wl[i]
         e=nm2eV(x)*shift
         cd_o_p = self.getCD_orig_phase()
         for j in range(len(self.wl_orig)):
            e0 = nm2eV(self.wl_orig[j])
            val = lorentz(e0,gamma,e)
#wrong            x0 = self.wl_orig[j]
#wrong            val = lorentz(x0,gamma,x)
            uv[i] = uv[i]+val*self.uv_orig[j]
            cd[i] = cd[i]+val*cd_o_p[j]
#         print "0", x, uv[i], cd[i]
#      for i in self.wl_orig:
#         print "1", i
      self.uv=uv
#      self.cd=[ a*self.phase for a in cd ]
      self.cd=cd

   def getLambdas(self):
      return self.wl

   def getUV(self):
      return self.uv

   def getCD(self):
      return self.cd

   def SpectrumThfactory(wl, uv, cd, phase, lambdaMin, lambdaMax, gamma, shift):
      logging.info( "Initialization of Theoretical Spectrum")
      spectrumTh = Spectrum(wl=wl, uv=uv, cd=cd, phase=phase)
      logging.info( "  setting range ...")
      spectrumTh.setRange(lambdaMin, lambdaMax)
      logging.info( "  computing spectrum ...")
      spectrumTh.compute_spectrum(gamma=gamma, shift=shift)
      x=spectrumTh.getLambdas()   
      uv_th=spectrumTh.getUV()   
      cd_th=spectrumTh.getCD()   
      logging.info( "Theoretical spectra computed between {0} and {1} at {2} values".format(min(x), max(x), len(x)))
      logging.info( "   UV spectrum: max {0} min {1} at {2} pts.".format(min(uv_th), max(uv_th), len(uv_th)))
      logging.info( "   CD spectrum: max {0} min {1} at {2} pts.".format(min(cd_th), max(cd_th), len(cd_th)))
      return spectrumTh
   SpectrumThfactory=staticmethod(SpectrumThfactory)

def read_tm_spectrum(fn):
   """Returns 3 lists in from a TURBOMOLE escf output name fn:
   excitation wavelengths in nm
   uv intensity in velocity representation
   cd intensity in velocity representation"""
   f = open(fn, 'r')
   lines=f.readlines()
   wl=[]
   uv=[]
   cd=[]
   for l in lines:
      if bool(re.search('Excitation energy...nm', l)):
         val=float(l.split()[4])
         wl.append(val)
      if bool(re.search('velocity representation', l)):
         val=float(l.split()[2])
         if len(uv)==len(cd) :
            uv.append(val)
         else:
            cd.append(val)
   return wl, uv, cd

def read_csv_spectrum(fn):
   """Returns 2 lists from a csv file
      _wavelengths in nm
      _absorption values"""
   f = open(fn, 'r')
   lines=f.readlines()
   wl=[]
   uv=[]
   for l in lines:
      li=l.split()
      if (len(li)<2):
         break
      wl.append(float(li[0]))
      uv.append(float(li[1]))
   return wl, uv

def nm2eV(l):
   h=constants.value("Planck constant in eV s")
   c=constants.value("speed of light in vacuum")
   return 1e9*h*c/(1.0*l)

def eV2nm(e):
   h=constants.value("Planck constant in eV s")
   c=constants.value("speed of light in vacuum")
   return 1e-9*h*c/(1.0*e)

def lorentz(x0,gamma,x):
   """Value of a lorentzian function at x of fwhw gamma centered on x0"""
   return (gamma*0.5)/(math.pow((x-x0),2)+math.pow(gamma*0.5,2))

def main():
   print "Spectrum library"
   h=constants.value("Planck constant in eV s")
   c=constants.value("speed of light in vacuum")
   print "Planck constant in eV s {0}",h
   print "Speed of light in vaccuum",c
   print "lambda (nm) | E(eV)"
   for l in range(100,1100,100):
      print l,nm2eV(l)
   print "E(eV) | lambda (nm)"
   for e in range(1,11):
      print e,eV2nm(e)

if __name__ == '__main__':
    main()
