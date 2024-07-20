import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
import os.path

def resize_nearest_neighbor(image, scale_factor):
    """Función que rescala una imagen en cierto factor de escala utilizando el método nearest neighbor
    
    Args:
        image (np.array): Imagen a reescalar en formato matriz
        scale_factor (int): Numero entero por el cual se realizará el rescaleo
    
    Returns:
        new_image (np.array): Imagen reescalada habiendo utilizado el método nearest neighbor

    """
    # Obtener dimensiones originales de la imagen
    Nx, Ny = image.shape
    
    # Calcular nuevas dimensiones de la imagen escalada
    Mx = int(Nx * scale_factor)
    My = int(Ny * scale_factor)
    
    # Crear una nueva matriz para la imagen escalada
    new_image = np.zeros((Mx, My), dtype=np.uint8)
    
    # Iteramos sobre las coordenadas de la imagen reescalada
    for jy in range(My):
        for jx in range(Mx):
            # Calculamos la parametrización en la imágen sin escalar
            x = jx/Mx * Nx
            y = jy/My * Ny

            # Vector de asignaciones
            asigna = [(int(x), int(y)), (int(x), int(y+1)), (int(x+1), int(y)), (int(x+1), int(y+1))]
            # Calculo todas las distancias y elijo la mínima
            distancias = [math.dist((x,y) , (int(x), int(y))) , math.dist((x,y), (int(x), int(y+1))), math.dist((x,y), (int(x+1), int(y))), math.dist((x,y), (int(x+1), int(y+1)))]
            idx = distancias.index(min(distancias))

            # Como esto puede darme un valor en el último pixel de la imagen pero los indices no van hasta ahí lo corrrijo
            if asigna[idx][0] == Nx:
                nearest_x = Nx - 1
            elif asigna[idx][1] == Ny:
                nearest_y = Ny - 1
            else:
                nearest_x = asigna[idx][0]
                nearest_y = asigna[idx][1]
            
            new_image[jx, jy] = image[nearest_x, nearest_y]

    # # Iterar sobre cada píxel de la imagen escalada
    # for jy in range(new_height):
    #     for jx in range(new_width):
    #         # Calcular las coordenadas del píxel más cercano en la imagen original
    #         nearest_i = min(int(jx / scale_factor), height - 1)
    #         nearest_j = min(int(jy / scale_factor), width - 1)
    #         # Asignar el valor del píxel más cercano en la imagen original al píxel correspondiente en la imagen escalada
    #         new_image[jx, jy] = image[nearest_i, nearest_j]
            
    return new_image


def resize_bilinear(image, scale_factor):
    """Función que rescala una imagen en cierto factor de escala utilizando el método bilinear
    
    Args:
        image (np.array): Imagen a reescalar en formato matriz
        scale_factor (float): Número flotante por el cual se realizará el reescalado
    
    Returns:
        new_image (np.array): Imagen reescalada habiendo utilizado el método bilinear
    """
    # Obtener dimensiones originales de la imagen
    Nx, Ny = image.shape[:2]

    # Calcular nuevas dimensiones de la imagen escalada
    Mx = int(Nx * scale_factor)
    My = int(Ny * scale_factor)

    # Crear una nueva matriz para la imagen escalada
    new_image = np.zeros((Mx, My, 3), dtype=np.uint8)
    
     # Iterate over the pixels of the scaled matrix
    for i in range(Mx):
        for j in range(My):
            x = i / Mx * Nx # Scale x to match image coordinates
            y = j / My * Ny

            # Calculate the indices of the neighboring pixels
            x1, y1 = int(np.floor(x)), int(np.floor(y))
            x2, y2 = min(x1 + 1, Nx - 1), min(y1 + 1, Ny - 1)
        
            # Calculate the fractional parts
            frac_x = x - x1
            frac_y = y - y1

            # Perform bilinear interpolation
            interpolated_value = (1 - frac_x) * (1 - frac_y) * image[x1, y1] + \
                                 frac_x * (1 - frac_y) * image[x2, y1] + \
                                 (1 - frac_x) * frac_y * image[x1, y2] + \
                                 frac_x * frac_y * image[x2, y2]
            
            new_image[i, j] = interpolated_value.astype(np.uint8)
                
    return new_image
    
    # # Iterar sobre cada píxel de la imagen escalada
    # for i in range(Mx):
    #     for j in range(My):
    #         # Calcular las coordenadas en la imagen original correspondientes al píxel actual en la imagen escalada
    #         y, x = i / scale_factor, j / scale_factor
    #         y1, x1 = int(np.floor(y)), int(np.floor(x))
    #         y2, x2 = min(y1 + 1, My - 1), min(x1 + 1, Mx - 1)
    #         # Calcular las fracciones de distancia entre los píxeles vecinos y el píxel actual
    #         dx, dy = x - x1, y - y1
    #         # Realizar la interpolación bilineal para obtener el valor del píxel actual en la imagen escalada
    #         new_image[i, j] = (1 - dx) * (1 - dy) * image[y1, x1] + dx * (1 - dy) * image[y1, x2] + (1 - dx) * dy * image[y2, x1] + dx * dy * image[y2, x2]
    # return new_image

def resize_bicubic(image, scale_factor):
    """Función que rescala una imagen en cierto factor de escala utilizando el método bicúbico

    Args:
        image (np.array): Imagen a reescalar en formato matriz
        scale_factor (int): Numero entero por el cual se realizará el rescaleo
    
    Returns:
        new_image (np.array): Imagen reescalada habiendo utilizado el método bicúbico
    """

    # Implementación de la interpolación bicúbica utilizando OpenCV
    return cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

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
    fig.colorbar(imgplot, ax=ax1)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

infile = 'ImagenC.pgm'
image = read_pgm_file(infile)

print('image.shape: ', image.shape)

# Factor de escala
scale_factor = 8

# Reescalar utilizando interpolación de primeros vecinos
resized_image_nn = resize_nearest_neighbor(image, scale_factor)

# Reescalar usando interpolación bilineal
resized_image_bilinear = resize_bilinear(image, scale_factor)

# Reescalar usando interpolación bicúbica
resized_image_bicubic = resize_bicubic(image, scale_factor)

save_plot_img(image, 'Original.pdf')
save_plot_img(resized_image_nn, 'NN_Resize.pdf')
save_plot_img(resized_image_bilinear, 'Bi_Resized.pdf')
save_plot_img(resized_image_bicubic, 'BiCu_Resized.pdf')
