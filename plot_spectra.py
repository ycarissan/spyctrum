#!/usr/bin/python

import re
import math
import numpy as np
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d

class Spectrum:
   def __init__(self):
      self.xmin = float('nan')
      self.xmax = float('nan')
      self.gamma= float('nan')
      self.dt   = float('nan')
      self.npts = 0
      self.orig = {}
      self.data = {}

   def getLambda():
      return self.data.keys()

   def getValue(typ, x):
      return self.orig[x][typ]

   def setXmin(xmin):
      self.xmin=xmin

   def getXmin():
      return self.xmin

   def setXmax(xmax):
      self.xmax=xmax

   def getXmax():
      return self.xmax

   def setGamma(gamma):
      self.gamma=gamma

   def getGamma():
      return self.gamma

   def setDt(dt):
      self.dt=dt

   def getDt():
      return self.dt

   def setNpts(npts):
      self.npts=npts

   def getNpts():
      return self.npts

   def getLambdaOrig(self):
      return sorted(self.orig.keys())

   def getValueOrig(self, typ, x):
      return self.orig[x][typ]

class SpectrumExperimental(Spectrum):
   def __init__(self, fn):
      Spectrum.__init__(self)
      self.get_spectrum_ref(fn)

   def get_spectrum_ref(self, fn):
      f = open(fn, 'r')
      lines=f.readlines()
      for l in lines:
         li=l.split()
         if (len(li)<2):
            break
         x=li[0]
         y=li[1]
         self.xmin=min(x,self.xmin)
         self.xmax=max(x,self.xmax)
         self.orig[x]={}
         self.orig[x]["uv"] = y

   def generate_spectrum(self, npts, xmin=None, xmax=None, dt=None):
      if xmin==None: xmin=self.xmin
      if xmax==None: xmax=self.xmax
      if dt==None: dt=self.dt
      xval = []
      uv   = []
      for k in sorted(self.orig.keys()):
         xval.append(float(k))
         uv.append(float(self.data[k]["uv"]))
      spectrum_interpolate = interp1d(xval, uv, kind='cubic')
      xnew = np.arange(xmin, xmax, dt)
      ynew = spectrum_ref_interpolate(xnew)
      for i in range(len(xnew)):
         self.data[xnew[i]]["uv"] = ynew

class SpectrumTheoretical(Spectrum):
   def __init__(self, fn="escf.out", npts=1000, gamma=50):
      Spectrum.__init__(self)
      osc_str = get_lambda(fn)
      xmin, xmax, dt = get_interval(osc_str, npts)
      self.xmin = xmin
      self.xmax = xmax
      self.orig = osc_str
      self.gamma= gamma
      self.dt   = dt

   def generate_spectrum(self, npts, xmin=None, xmax=None, dt=None, gamma=50):
      if xmin==None: xmin=self.xmin
      if xmax==None: xmax=self.xmax
      if dt==None: dt=self.dt
      for i in range(npts):
         x=xmin+i*dt
         val={}
         uv=cd=0
         for j in self.orig.keys():
            uv=uv+lorentz(j,self.gamma,x)*self.orig[j]["uv"]
            cd=cd+lorentz(j,self.gamma,x)*self.orig[j]["cd"]
         val["uv"]=uv
         val["cd"]=cd
         self.data[x]=val

def get_interval(data, npts):
   xmin=min(data.keys())
   xmax=max(data.keys())
   delta=(xmax-xmin)
   xmin=xmin-delta*.05
   xmax=xmax+delta*.05
   delta=(xmax-xmin)
   dt=delta/npts
   return xmin, xmax, dt

def get_lambda(fn):
   f = open(fn, 'r')
   lines=f.readlines()
   osc_str = {}
   for l in lines:
      if bool(re.search('Excitation energy...nm', l)):
         val=float(l.split()[4])
         strength={}
      if bool(re.search('velocity representation', l)):
         if len(strength)==0:
            strength["uv"] = float(l.split()[2])
         else:
            strength["cd"] = float(l.split()[2])
            osc_str[val] = strength
   return osc_str

def lorentz(x0,gamma,x):
   return (gamma/2)/(math.pow((x-x0),2)+gamma/2)

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
