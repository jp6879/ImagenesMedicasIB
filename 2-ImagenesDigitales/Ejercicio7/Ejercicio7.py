import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

def read_files(path):
    """ Función que lee los archivos de un directorio

    Args:
        path (str): Ruta del directorio

    Returns:
        files (list): Lista con los nombres de los archivos del directorio
    """
    files = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            file = os.path.join(path, file)
            files.append(file)
    return files

def read_csv(file):
    data = pd.read_csv(file)
    bins = data["value"]
    histo = data["count"]
    return bins, histo

def analiza_histogramas(path):
    files = read_files(path)
    for file in files:
        values = pd.read_csv(file)["value"]
        histo, bins = np.histogram(values, bins = 255)
        bins, histo = read_csv(file)
        prob = histo/np.sum(histo)
        mids = (bins[1:] + bins[:-1])/2
        mean = np.sum(mids*prob)
        std = np.sqrt(np.sum((mids - mean)**2*prob))
        print(f"El archivo {file[-12:-4]} tiene una media de {mean} y una desviación estándar de {std} y una relación señal ruido de {mean/std}")
        plt.bar(bins, histo, label = file[-12:-4], alpha = 0.6)
    
    plt.gca().xaxis.set_major_locator(plt.AutoLocator())
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_major_locator(plt.AutoLocator())
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_ticks_position('both')
    plt.gca().xaxis.set_ticks_position('both')
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=12)
    plt.grid(linestyle='--', linewidth=0.5)
    plt.xlabel('Intensidad', fontsize = 12)
    plt.ylabel("Frecuencia", fontsize = 12)
    plt.xlim(0, 120)
    plt.legend()
    plt.savefig("ComparacionHisto.pdf")
    plt.show()


if __name__ == "__main__":
    path = "C:/Users/Propietario/Desktop/ib/5-Maestría/Imágenes Médicas/Practicas/Practica2/Ejercicio7/"
    analiza_histogramas(path)


"""
El archivo  AAA0002 tiene una media de 56.88922712667004 y una desviación estándar de 4.147672460203824 y una relación señal ruido de 13.715940126061545
El archivo  AAA0003 tiene una media de 56.70381944444445 y una desviación estándar de 5.675830763534848 y una relación señal ruido de 9.990399962018934
El archivo  AAA0004 tiene una media de 56.574425574425575 y una desviación estándar de 7.364202184954213 y una relación señal ruido de 7.682356371205108
"""


"""
FMHW11 = 5
FMHW12 = 2
FMHW13 = 6
FMHW14 = 4
"""