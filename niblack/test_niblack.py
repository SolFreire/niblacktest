import numpy as np
from skimage import io, filters
from skimage.io import imread, imsave

WIDTH, HEIGHT = 89, 89
WINDOW_SIZE = 55
K = -0.1

image = imread('test_input.pgm', as_gray=True)
# Garante escala 0–255 em uint8
if image.dtype != np.uint8:
    image = (image * 255).astype(np.uint8)

# Calcula o threshold adaptativo com Niblack
thresh = filters.threshold_niblack(image, window_size=WINDOW_SIZE, k=K)
binary_sk = image > thresh
binary_sk = (binary_sk * 255).astype(np.uint8)  


with open('out_python.pgm', 'w') as f:
    f.write("P2\n")
    f.write("# Binarização Niblack em Python\n")
    f.write(f"{WIDTH} {HEIGHT}\n")
    f.write("255\n")
    for row in binary_sk:
        f.write(" ".join(str(pixel) for pixel in row) + "\n")

img_c = imread('out_c.pgm', as_gray=True)
if img_c.dtype != np.uint8:
    img_c = (img_c * 255).astype(np.uint8)

diff = binary_sk != img_c
diff_map = (diff * 255).astype(np.uint8)
n_diff = np.sum(diff)
total = WIDTH * HEIGHT
acc = 100.0 * (1 - n_diff / total)

with open('mapa_diferencas.pgm', 'w') as f:
    f.write("P2\n")
    f.write("# Mapa de diferenças entre Python e C\n")
    f.write(f"{WIDTH} {HEIGHT}\n")
    f.write("255\n")
    for row in diff_map:
        f.write(" ".join(str(pixel) for pixel in row) + "\n")

if n_diff > 0:
    coords = np.argwhere(diff)
    print("Exemplos de diferenças:")
    for y, x in coords[:]:  # Mostra no máximo 10 diferenças
        print(f" Pixel[{y},{x}]: sk={binary_sk[y,x]} vs c={img_c[y,x]}")

print(f"Diferenças: {n_diff}/{total} — Acurácia: {acc:.2f}%")
