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

def convolution2d(image, kernel):
    m, n = kernel.shape
    if (m == n):
        y, x = image.shape
        y = y - m + 1
        x = x - m + 1
        new_image = np.zeros((y,x))
        for i in range(y):
            for j in range(x):
                new_image[i][j] = np.sum(image[i:i+m, j:j+m]*kernel)
    return new_image

def save_plot_img(im, filename):
    fig = plt.figure()
    ax1 = plt.subplot(1, 1, 1)
    vmin = np.amin(im)
    vmax = np.max(im)
    imgplot = ax1.imshow(im,cmap='gray', vmin=vmin, vmax=vmax)
    ax1.set_xlabel('x', fontsize = 12)
    ax1.set_ylabel('y', fontsize = 12)
    fig.colorbar(imgplot, ax=ax1)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    file_name = 'ImagenC.pgm'
    image = read_pgm_file(file_name)

    print(image.shape)

    # Creamos un filtro pasa bajo 3x3
    h1 = 1/9 * np.ones((3,3))

    # Creamos un filtro pasa bajo 5x5
    h2 = 1/25 *np.ones((5,5))

    # Creamos un filtro pasa bajos 7x7
    h3 = 1/49 *np.ones((7,7))

    out_names = ['FiltroC1.pdf', 'FiltroC2.pdf', 'FiltroC3.pdf']
    filtros = [h1, h2, h3]

    for i in range(3):
        img_filtro = convolution2d(image, filtros[i])
        out_name = out_names[i]
        save_plot_img(img_filtro, out_name)


