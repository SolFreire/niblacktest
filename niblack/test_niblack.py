import numpy as np

def read_pgm(fn):
    with open(fn) as f:
        assert f.readline().strip() == 'P2'
        while True:
            l = f.readline()
            if not l.startswith('#'): break
        w,h = map(int,l.split())
        maxv = int(f.readline())
        data = np.loadtxt(f, dtype=int)
    return data.reshape((h,w))

in_img  = read_pgm('test_image.pgm')
out_img = read_pgm('out.pgm')

x,y = 44,44
patch = in_img[y-7:y+8, x-7:x+8]   
mu   = patch.mean()
sigma= patch.std(ddof=1)
T    = mu + (-0.2)*sigma
calc = 0 if in_img[y,x]<T else 255
print("pixel[44,44]: in=", in_img[y,x],
      "T=",round(T,2),
      "=> manuel:", calc,
      " vs code:", out_img[y,x])
