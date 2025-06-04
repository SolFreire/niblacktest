import numpy as np

def read_pgm(fn):
    with open(fn) as f:
        assert f.readline().strip() == 'P2'
        while True:
            l = f.readline()
            if not l.startswith('#'): break
        w, h = map(int, l.split())
        maxv = int(f.readline())
        data = np.loadtxt(f, dtype=int)
    return data.reshape((h, w))


in_img  = read_pgm('test_image.pgm')  
out_img = read_pgm('out.pgm')         


def niblack_python(image, window_size=15, k=-0.2):
    h, w = image.shape
    pad = window_size // 2
    padded = np.pad(image, pad, mode='edge')
    result = np.zeros_like(image)

    for y in range(h):
        for x in range(w):
            patch = padded[y:y+window_size, x:x+window_size]
            mu = patch.mean()
            sigma = patch.std(ddof=1)
            T = mu + k * sigma
            result[y, x] = 0 if image[y, x] < T else 255
    return result

ref_img = niblack_python(in_img)


dif = ref_img != out_img
n_dif = np.sum(dif)
total = ref_img.size
acc = 100 * (1 - n_dif / total)

print(f"Diferenças encontradas: {n_dif}/{total}")
print(f"Acurácia comparada ao Python: {acc:.2f}%")


if n_dif > 0:
    diff_coords = np.argwhere(dif)
    print("Exemplos de diferenças (no máximo 10):")
    for y, x in diff_coords[:10]:
        print(f"Pixel[{y},{x}]: Python={ref_img[y,x]} vs C={out_img[y,x]}")
