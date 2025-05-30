import numpy as np
import matplotlib.pyplot as plt

def read_pgm(fn):
    with open(fn) as f:
        assert f.readline().strip() == 'P2'
        while True:
            pos = f.tell()
            line = f.readline()
            if not line.startswith('#'):
                f.seek(pos)
                break
        w, h = map(int, f.readline().split())
        maxv = int(f.readline())
        data = np.loadtxt(f, dtype=int)
    return data.reshape((h, w))

if __name__ == "__main__":
    in_img  = read_pgm('test_image.pgm')
    out_img = read_pgm('out.pgm')

    x, y = 44, 44
    patch  = in_img[y-7:y+8, x-7:x+8]
    mu     = patch.mean()
    sigma  = patch.std(ddof=1)
    T      = mu + (-0.2) * sigma
    calc   = 0 if in_img[y, x] < T else 255
    print(f"pixel[44,44]: in={in_img[y,x]}  T={T:.2f}  => manual={calc} vs code={out_img[y,x]}")

    plt.figure(figsize=(8,4))
    plt.subplot(1,2,1)
    plt.title('Gradient (89×89)')
    plt.imshow(in_img, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    plt.subplot(1,2,2)
    plt.title('Niblack Output')
    plt.imshow(out_img, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    plt.tight_layout()
    plt.savefig('comparison.png', dpi=150)
    plt.show()
