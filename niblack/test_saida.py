import numpy as np
from skimage import io, filters
from skimage.io import imread, imsave

#Dimensões da imagem escolhida pelo professor
WIDTH, HEIGHT = 89, 89
#tamanho da janela iusada e constante da formula de niblack
WINDOW_SIZE = 15
K = -0.2




img_c = imread('out_c.pgm', as_gray=True)
if img_c.dtype != np.uint8:
    img_c = (img_c * 255).astype(np.uint8)

img_stm = imread('out_stm.pgm', as_gray=True)
if img_stm.dtype != np.uint8:
    img_stm = (img_c * 255).astype(np.uint8)

diff = img_stm != img_c
diff_map = (diff * 255).astype(np.uint8)
n_diff = np.sum(diff)
total = WIDTH * HEIGHT
acc = 100.0 * (1 - n_diff / total)

if n_diff > 0:
    coords = np.argwhere(diff)
    print("Exemplos de diferenças:")
    for y, x in coords[:]:  
        print(f" Pixel[{y},{x}]: sk={img_stm[y,x]} vs c={img_c[y,x]}")

print(f"Diferenças: {n_diff}/{total} — Acurácia: {acc:.2f}%")
