import cv2
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



def transformacion_binaria(img):
    """ Función que realiza una trasnformación binaria a una imagen
    T(pixel) = 1 si 0 < r < 128
    T(pixel) = 0 si r >= 128
    Args:
        img (np.array): Imagen en formato de array de numpy
    
    Returns:
        imout (np.array): Imagen transformada
    """
    pixels = img.flatten()
    s = np.zeros(len(pixels))
    for i, r in enumerate(pixels):
        if 0 < r < 128:
            s[i] = 1
        elif r >= 128:
            s[i] = 0
    imout = s.reshape(img.shape)
    return imout

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

def gamma_transform(img, gamma):
    """Función que realiza una trasnformación gamma a una imagen
    T(pixel) = s_max * (r/r_max) ** gamma
    Args:
        img (np.array): Imagen en formato de array de numpy
        gamma (float): Valor de gamma
    
    Returns:
        imout (np.array): Imagen transformada
    """
    pixels = img.flatten()
    s = np.zeros(len(pixels))
    s_max = 255
    r_max = max(pixels)
    for i, r in enumerate(pixels):
        s[i] = s_max * (r/r_max) ** gamma
    
    imout = s.reshape(img.shape)
    return imout


def resta(img1, img2):
    return img1 - img2

if __name__ == "__main__":
    # Leemos la imagen A
    infile = 'ImagenA.pgm'
    img = read_pgm_file(infile)

    # Hacemos la trasformación 1
    T1_img = transformacion_binaria(img)
    # Guardamos la imagen
    save_plot_img(T1_img, 'Out_ImagenATransformacion1.pdf')

    # Hacemos una lista con los gamma para la transformación gamma
    gammas = [0.2, 0.5, 2, 3]
    # Hacemos una lista con las imagenes aplicando la trasformacion gamma
    images_gamma = []

    # Hacemos la trasformación gamma
    for gamma in gammas:
        images_gamma.append(gamma_transform(img, gamma))

    # Graficamos en la misma figura las cuatro imagenes de la trasformación gamma

    fig = plt.figure(figsize=(8,6))
    for i, im in enumerate(images_gamma):
        ax = plt.subplot(2, 2, i+1)
        vmin = np.amin(im)
        vmax = np.max(im)
        imgplot = ax.imshow(im,cmap='gray', vmin=vmin, vmax=vmax)
        if i == 0 or i == 2:
            ax.set_ylabel('y', fontsize = 12)
        if i == 2 or i == 3:
            ax.set_xlabel('x', fontsize = 12)
        ax.set_title('$\gamma$ = {}'.format(gammas[i]))

    plt.savefig('Out_ImagenATransformacionGamma.pdf')
    plt.show()

    # Para la resta usamos solo la primera trasformación y las gamma con 0.2 y 3

    # Hacemos las tres restas y guardamos las imágenes

    resta_img1 = resta(img, T1_img)
    save_plot_img(resta_img1, 'Out_ImagenAResta1.pdf')

    resta_img = resta(T1_img, images_gamma[0])
    save_plot_img(resta_img, 'Out_ImagenARestaGAMMA0.2.pdf')

    resta_img = resta(T1_img, images_gamma[3])
    save_plot_img(resta_img, 'Out_ImagenARestaGAMMA3.pdf')


