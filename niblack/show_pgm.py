import numpy as np
import matplotlib.pyplot as plt

def read_pgm(fn):
    with open(fn) as f:
        f.readline()           # P2
        f.readline()           # comentário
        w,h = map(int, f.readline().split())
        f.readline()           # maxval
        data = np.loadtxt(f, dtype=np.uint8)
    return data.reshape((h,w))

g = read_pgm('gradient.pgm')
o = read_pgm('out.pgm')

plt.figure(figsize=(8,4))
plt.subplot(1,2,1)
plt.title('Gradient (89×89)')
plt.imshow(g)
plt.axis('off')

plt.subplot(1,2,2)
plt.title('Niblack Output')
plt.imshow(o)
plt.axis('off')

plt.tight_layout()
plt.savefig('comparison.png', dpi=150)
plt.show()
