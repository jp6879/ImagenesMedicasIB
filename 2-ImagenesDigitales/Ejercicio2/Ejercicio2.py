import cv2
import sys 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
import os.path

def read_pgm_file(file_name, path = r'C:\Users\Propietario\Desktop\ib\5-Maestría\Imágenes Médicas\Practicas\Practica2\archivos-practica2\\'):
    """ Función que lee un archivo .pgm

    Args:
        file_name (str): Nombre del archivo .pgm
        path (str): Ruta donde se encuentra el archivo .pgm

    Returns:
        img (np.array): Imagen en formato de array de numpy
    """
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

def show_img_hist(im, eqimg, fileout = 'Out_ImagenAHist.pdf'):
    """
    Función que calcula y muestra el histograma de la imagen cargada

    Args:
        im (np.array): Imagen a la que se le calculará el histograma
    
    Returns:
        None: Simplemente muestra el histograma junto con la imágen
    """

    # Calculamos el valor mínimo y máximo de la intensidad de la imagen
    vmin = np.amin(eqimg)
    vmax = np.max(eqimg)

    # Calculamos el número de niveles de intensidad
    L = vmax - vmin

    fig = plt.figure(figsize=(6,8))
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2)

    imgplot = ax1.imshow(eqimg,cmap='gray', vmin=vmin, vmax=vmax)
    ax1.set_xlabel('x', fontsize = 12)
    ax1.set_ylabel('y', fontsize = 12)
    fig.colorbar(imgplot, ax=ax1)
    pixels = im.flatten()
    eq_pixels = eqimg.flatten()
    # ravel() hace que la matriz de la imagen se convierta en un vector de una sola dimensión y luego calculamos el histograma
    hist, bin_edges = np.histogram(pixels,bins=256,range=(0,256))
    hist2, bin_edges2 = np.histogram(eq_pixels,bins=256,range=(0,256))

    ax2.bar(bin_edges[2:], hist[1:], alpha=1, label='Original')
    ax2.bar(bin_edges2[2:], hist2[1:], alpha=1, label='Ecualizada')
    ax2.set_xlabel('Intensidad', fontsize = 12)
    ax2.set_ylabel('Frecuencia', fontsize = 12)
    plt.legend()
    plt.savefig(fileout)
    plt.show()

def equalize_histogram(img):
    """
    Función que ecualiza el histograma de la imagen cargada

    Args:
        im (np.array): Imagen a la que se le calculará el histograma ecualizado
    
    Returns:
        imout (np.array): Imagen con el histograma ecualizado
    """

    pixels = img.flatten()
    print("Pixels: ", pixels)
    # Construimos su histograma con 256 bins proque sabemos que la imagen tiene esta escala de grises
    hist, bins = np.histogram(pixels, bins=256, range=(0,256))
    print("Bins", bins)
    # Para calcular la primitiva del histograma, necestiamos calcular la suma acumulada del histograma
    T = hist.cumsum()

    # Tenemos que perdir que esta primitiva esté normalizada por un factor tal que T(r_max) = S_max, donde S son los pixeles transformados, en este caso queremos que
    # S_max = 255, mientras que r_max = max(pixels)

    # Normalizamos la primitiva
    r_max = max(pixels)
    T = T * 255 / T[r_max]

    # Ahora al a nueva imagen le asignamos a cada pixel su valor transformado
    s_pixels = np.zeros(len(pixels))

    # Ubicamos donde estan los pixeles en el histograma y les asignamos su valor transformado
    for i, pixel in enumerate(pixels):
        idx, = np.where(bins == pixel)
        s_pixels[i] = T[idx]

    # La imagen transformada la devolvemos a su forma original de 217 x 181 pixels
    imout = s_pixels.reshape(img.shape)

    return imout


if __name__ == "__main__":
    
    infile = 'ImagenA.pgm'
    outfile = 'Out_ImagenA.pgm'
    
    img = read_pgm_file(infile)

    # La imágen es de 217 x 181 pixeles y la tenemos como un array
    im = np.array(img)
    print(f"Size of image: {im.shape}")

    imout = equalize_histogram(im)
    
    show_img_hist(im, imout, 'EQHist_ImagenA.pdf')

    cv2.imwrite(outfile,imout,[cv2.IMWRITE_PXM_BINARY,0])