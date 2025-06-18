import numpy as np
from skimage import io, filters
from skimage.io import imread, imsave

WIDTH, HEIGHT = 89, 89
WINDOW_SIZE = 51
K = -0.1

image = imread('test_input.pgm', as_gray=True)
# Garante escala 0–255 em uint8
if image.dtype != np.uint8:
    image = (image * 255).astype(np.uint8)

# Calcula o threshold adaptativo com Niblack
thresh = filters.threshold_niblack(image, window_size=WINDOW_SIZE, k=K)
binary_sk = image > thresh
binary_sk = (binary_sk * 255).astype(np.uint8)

imsave('out_python.pgm', binary_sk)

# Compara com resultado em C
img_c = imread('out_c.pgm', as_gray=True).astype(np.uint8)
diff = binary_sk != img_c
n_diff = np.sum(diff)
total = WIDTH * HEIGHT
acc = 100.0 * (1 - n_diff / total)

print(f"Diferenças: {n_diff}/{total} — Acurácia: {acc:.2f}%")
if n_diff > 0:
    coords = np.argwhere(diff)
    print("Exemplos de diferenças (até 10):")
    for y, x in coords[:10]:
        print(f" Pixel[{y},{x}]: sk={binary_sk[y,x]} vs c={img_c[y,x]}")
