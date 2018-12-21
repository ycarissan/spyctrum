from tkinter import *
from tkinter.filedialog import askopenfilename
from spyctrum import *
from spyctrum.spectrum import *
import matplotlib.pyplot as plt

def main():
    #
    # Define the root window
    #
    root = Tk()
    root.title("SpyGui")
    #
    filename = askopenfilename(
        title = "Choose the file to import",
        filetypes = (
            ("Turbomole escf output",("*.log", "*.out")),
            ("Orca output",("*.log", "*.out")),
            ("Orca output sTDA/sTDDFT",("*.log", "*.out")),
            ("all files","*")
        )
    )
    wl, uv, cd = read_tm_spectrum(filename)
    spectrumTh = Spectrum.SpectrumThfactory(wl, uv, cd, 1.0, min(wl) , max(wl), 0.2, 1.0)
    x1 = spectrumTh.getLambdas()
    y1 = spectrumTh.getUV()
    y2 = spectrumTh.getCD()
    #
    plt.subplot(2, 1, 1)
    plt.plot(x1, y1, 'o-')
    plt.title('UV and CD spectra')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel(' UV Absorbance')
    #
    fig, ax = plt.subplot(2, 1, 2)
    plt.plot(x1, y2, '.-')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('ECD Absorbance')

    plt.show()

    root.mainloop()

if __name__ == '__main__':
    main()


