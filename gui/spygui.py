from tkinter import *
import matplotlib.pyplot as plt
from spectrum import *

def main():
#
# Define the root window
#
   root = Tk()
   root.title("SpyGui")
#

#
   plt.subplot(2, 1, 1)
   plt.plot(x1, y1, 'o-')
   plt.title('A tale of 2 subplots')
   plt.xlabel('Wavelength (nm)')
   plt.ylabel(' UV Absorbance')
#
   plt.subplot(2, 1, 2)
   plt.plot(x2, y2, '.-')
   plt.xlabel('Wavelength (nm)')
   plt.ylabel('ECD Absorbance')

   plt.show()

   root.mainloop()

if __name__ == '__main__':
    main()

    wl, uv, cd = read_tm_spectrum(refuvcsv)
    spectrumTh = Spectrum.SpectrumThfactory(wl, uv, cd)
