from skimage.io import imread
import numpy as np


img_sk = imread('out_python_sk.pgm', as_gray=True)
if img_sk.dtype != np.uint8:
    img_sk = (img_sk * 255).astype(np.uint8)

img_cv = imread('out_python_cv.pgm', as_gray=True)
if img_cv.dtype != np.uint8:
    img_cv = (img_cv * 255).astype(np.uint8)


bin_sk = (img_sk > 127).astype(np.uint8)
bin_cv = (img_cv > 127).astype(np.uint8)


diff = (bin_sk != bin_cv)
diff_map = (diff * 255).astype(np.uint8)
n_diff = np.sum(diff)
total = 89 * 89
acc = 100.0 * (1 - n_diff / total)

if n_diff > 0:
    coords = np.argwhere(diff)
    print("Exemplos de diferenças:")
    for y, x in coords[:]:  
        print(f" Pixel[{y},{x}]: cv={img_cv[y,x]} vs sk={img_sk[y,x]}")

print(f"Diferenças: {n_diff}/{total} — Acurácia: {acc:.2f}%")