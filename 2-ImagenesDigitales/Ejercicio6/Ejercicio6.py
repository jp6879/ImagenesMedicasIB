import cv2
import sys 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
import os.path
from PIL import Image, ImageFilter 

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

def save_plot_img(im, filename):
    fig = plt.figure()
    ax1 = plt.subplot(1, 1, 1)
    vmin = np.amin(im)
    vmax = np.max(im)
    imgplot = ax1.imshow(im,cmap='gray', vmin=vmin, vmax=vmax)
    ax1.set_xlabel('x', fontsize = 12)
    ax1.set_ylabel('y', fontsize = 12)
    plt.title(filename)
    fig.colorbar(imgplot, ax=ax1)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

def add_gaussian_nosie(img):
    """ Función que agrega ruido gaussiano a una imagen

    Args:
        img (np.array): Imagen en formato de array de numpy

    Returns:
        img (np.array): Imagen en formato de array de numpy con ruido gaussiano
    """
    rows, columns = img.shape
    # Agregamos ruido gaussiano
    mean = 0
    sigma = 3
    gauss = np.random.normal(mean, sigma, (rows, columns))
    noisy_img = img + gauss
    return noisy_img


def gaussian_blur(img):
    """ Función que agrega un filtro pasa bajos gaussiano a la imagen

    Args:
        img (np.array): Imagen en formato de array de numpy

    Returns:
        img (np.array): Imagen en formato de array de numpy con el filtro aplicado
    """
    # Aplicamos un filtro gaussiano a la imagen
    img_gausian_blur = cv2.GaussianBlur(img, (9, 9), cv2.BORDER_DEFAULT)
    return img_gausian_blur

def unsharp_method(img):
    """ Función que aplica el método de unsharp a una imagen

    Args:
        img (np.array): Imagen en formato de array de numpy
        noisy_img (np.array): Imagen en formato de array de numpy con ruido gaussiano

    Returns:
        img (np.array): Imagen en formato de array de numpy con el método de unsharp
    """
    # Aplicamos el método de unsharp
    img_unsharp = img - gaussian_blur(img)
    return img_unsharp

def high_boost(img, A):
    """ Función que aplica el método de high boost a una imagen
    
    Args:
        img (np.array): Imagen en formato de array de numpy
        A (float): Valor de A para el método de high boost
    
    Returns:
        img (np.array): Imagen en formato de array de numpy con el método de high boost
    """
    # Aplicamos el filtro high boost
    img_hb = A * img - gaussian_blur(img)
    return img_hb

def diferencia_absoluta(img, noisy_img , A):
    """ Función que calcula la diferencia absoluta entre la imagen original sin ruido y la imagen filtrada

    Args:
        img (np.array): Imagen en formato de array de numpy
        img_filtered (np.array): Imagen en formato de array de numpy filtrada
    
    Returns:
        img (np.array): Imagen en formato de array de numpy con la diferencia absoluta
    """
    img_hb = high_boost(noisy_img, A)
    diff_hb = np.abs(img - img_hb)
    
    return np.sum(diff_hb)

if __name__ == '__main__':
    file_name = 'ImagenA.pgm'

    image = read_pgm_file(file_name)

    save_plot_img(image, 'Original_ImageA.pdf')

    noisy_image = add_gaussian_nosie(image)

    save_plot_img(noisy_image, 'GaussianNoise_ImageA.pdf')

    unsharp_image = unsharp_method(noisy_image)

    save_plot_img(unsharp_image, 'Unsharp_NoisyImageA.pdf')

    As = np.linspace(0, 8, 17)

    high_boost_image = high_boost(noisy_image, 2)
    save_plot_img(high_boost_image, 'HighBoost_NoisyImageA-A2.pdf')

    hb_diffs = []
    for A in As:
        hb = diferencia_absoluta(image, noisy_image , A)
        hb_diffs.append(hb)

    print(hb_diffs[0] - min(hb_diffs))

    plt.plot(As, hb_diffs, label='Diferencia absoluta')
    plt.xlabel('A', fontsize = 12)
    plt.ylabel('Diferencia absoluta', fontsize = 12)
    plt.legend()
    plt.gca().xaxis.set_major_locator(plt.AutoLocator())
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_major_locator(plt.AutoLocator())
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_ticks_position('both')
    plt.gca().xaxis.set_ticks_position('both')
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=12)
    plt.legend(fontsize=10, loc = "best")
    plt.grid(linestyle='--', linewidth=0.5)
    plt.savefig('DiferenciaAbsolutaVsA.pdf', bbox_inches='tight')
    plt.show()
