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
    in_img  = read_pgm('test_input.pgm')
    out_img = read_pgm('out_c.pgm')

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
