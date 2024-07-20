import cv2
import sys 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
import os.path

def read_pgm_file(file_name, path = r'C:\Users\Propietario\Desktop\ib\5-Maestría\Imágenes Médicas\Practicas\Practica2\archivos-practica2\\'):

    # Para abrir la imagen hay que cambiar el directorio a la carpeta donde está la imagen
    data_dir = os.path.dirname(path)

    # Vemos si la imagen existe
    file_path = os.path.join(data_dir, file_name)
    assert os.path.isfile(file_path), 'file \'{0}\' does not exist'.format(file_path)

    # Leemos la imágen utilizando OpenCV, con la bandera cv2.IMREAD_GRAYSCALE que indica que se leerá en escala de grises
    img = cv2.imread(file_name,flags=cv2.IMREAD_GRAYSCALE)

    # Si la imagen se leyó correctamente, mostramos su tamaño sinó mostramos un mensaje de error
    if img is not None:
        print('img.size: ', img.size)
    else:
        print('imread({0}) -> None'.format(file_path))

    return img

def show_img_hist(im, fileout = 'Out_ImagenAHist.pdf'):
    """
    Función que calcula y muestra el histograma de la imagen cargada

    Args:
        im (np.array): Imagen a la que se le calculará el histograma
    
    Returns:
        None: Simplemente muestra el histograma junto con la imágen
    """

    # Calculamos el valor mínimo y máximo de la intensidad de la imagen
    vmin = np.amin(im)
    vmax = np.max(im)

    print("Intensity Min: {}   Max:{}".format(vmin,vmax))

    # Calculamos el número de niveles de intensidad
    L = vmax - vmin
    print("Number of Levels: {}".format(L))
    fig = plt.figure(figsize=(6,8))
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)
    imgplot = ax1.imshow(im,cmap='gray', vmin=vmin, vmax=vmax)
    ax1.set_xlabel('x', fontsize = 12)
    ax1.set_ylabel('y', fontsize = 12)
    fig.colorbar(imgplot, ax=ax1)
    # cv2.imshow(infile,img)
    # cv2.waitKey(0)
    
    # ravel() hace que la matriz de la imagen se convierta en un vector de una sola dimensión y luego calculamos el histograma
    hist, bin_edges = np.histogram(im.ravel(),bins=L)
    print("Histogram: ", len(hist))
    print("Bin Edges: ", len(bin_edges))
    ax2.bar(bin_edges[2:], hist[1:])
    ax2.set_xlabel('Intensidad', fontsize = 12)
    ax2.set_ylabel('Frecuencia', fontsize = 12)
    plt.savefig(fileout)
    plt.show()
    


def process_pgm_file(im):
    """
    Como primer procesamiento vamos a hacer un contras stretching de la imagen
    es decir una trasnformacion semilineal T(r) = a * r + b, donde si T(r) > 255 entonces T(r) = 255
    y si T(r) < 0 entonces T(r) = 0

    Args
        im (np.array): Imagen a la que se le aplicará el procesamiento

    Returns
        imout (np.array): Imagen procesada

    """
    im_copy = im.copy()

    # vmin = np.amin(im)
    # vmax = np.max(im)
    # L = vmax - vmin

    # hist, bin_edges = np.histogram(im_copy.ravel(),bins=L)
    
    a = 2
    b = -95

    def constrast_stretching(x):
        result = a * x + b
        if result > 255:
            result = 255
        elif result < 0:
            result = 0
        return result

    # recta = [constrast_stretching(x) for x in bin_edges]

    # plt.bar(bin_edges[:-1],hist)
    # plt.plot(recta, color = 'r')
    # plt.xlim([0,150])
    # plt.show()
    
    # Aplicamos la transformación a la imagen

    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            im_copy[i,j] = constrast_stretching(im[i,j])

    imout = im_copy
    
    return imout

if __name__ == "__main__":
    
    infile = 'ImagenA.pgm'
    outfile = 'Out_ImagenA.pgm'
    
    img = read_pgm_file(infile)

    # La imágen es de 217 x 181 pixeles y la tenemos como un array
    im = np.array(img)
    print(f"Size of image: {im.shape}")

    show_img_hist(im, 'ImagenAHist.pdf')

    imout = process_pgm_file(im)

    show_img_hist(imout, 'Out_ImagenAHist.pdf')

    cv2.imwrite(outfile,imout,[cv2.IMWRITE_PXM_BINARY,0])
