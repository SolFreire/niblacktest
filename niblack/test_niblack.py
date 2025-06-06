import numpy as np

WIDTH  = 89
HEIGHT = 89
WINDOW_SIZE = 51
K = -0.1


def read_pgm(fn):
    with open(fn, 'r') as f:
        magic = f.readline().strip()
        if magic != 'P2':
            raise ValueError(f"Arquivo {fn} não está no formato P2")

        while True:
            pos = f.tell()
            line = f.readline()
            if not line:
                raise ValueError("EOF inesperado lendo header PGM")
            if line.startswith('#'):
                continue
            else:
                f.seek(pos)
                break

        w, h = map(int, f.readline().split())
        maxv = int(f.readline())
        if (w, h) != (WIDTH, HEIGHT) or maxv != 255:
            raise ValueError(f"Dimensões inesperadas em {fn}: {w}x{h}, maxv={maxv}")

        data = np.loadtxt(f, dtype=int)
        if data.size != w * h:
            raise ValueError(f"Número de pixels lidos ({data.size}) != esperado ({w*h})")
        img = data.reshape((h, w))
        return img


def write_pgm(fn, img):
    h, w = img.shape
    if (h, w) != (HEIGHT, WIDTH):
        raise ValueError(f"Tamanho de saída {h}x{w} não corresponde a {HEIGHT}x{WIDTH}")
    with open(fn, 'w') as f:
        f.write("P2\n")
        f.write("# Niblack binarization (Python equivalente ao C)\n")
        f.write(f"{w} {h}\n")
        f.write("255\n")
        for y in range(h):
            row = img[y, :].astype(int)
            linha = " ".join(str(v) for v in row)
            f.write(linha + "\n")


def niblack_python_equivalente(image, window_size=WINDOW_SIZE, k=K):
    h, w = image.shape
    half = window_size // 2
    out = np.zeros_like(image, dtype=np.uint8)

    for y in range(h):
        y1 = max(y - half, 0)
        y2 = min(y + half, h - 1)

        for x in range(w):
            x1 = max(x - half, 0)
            x2 = min(x + half, w - 1)

            patch = image[y1:y2+1, x1:x2+1]

            mu = patch.mean()
            sigma = patch.std(ddof=1) if patch.size > 1 else 0.0

            T = mu + k * sigma
            out[y, x] = 0 if image[y, x] < T else 255

    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Uso: python3 niblack_equivalente.py entrada.pgm saida_c.pgm saida_python.pgm")
        print("  - entrada.pgm: arquivo P2 89x89, maxv=255")
        print("  - saida_c.pgm: resultado gerado pelo programa C")
        print("  - saida_python.pgm: será gerado por este script em Python")
        sys.exit(1)

    fn_entrada    = sys.argv[1]
    fn_saida_c    = sys.argv[2]  
    fn_saida_py    = sys.argv[3]

    img_in = read_pgm(fn_entrada)

    img_py_out = niblack_python_equivalente(img_in)

    write_pgm(fn_saida_py, img_py_out)
    print(f"Imagem Python escrita em: {fn_saida_py}")

    try:
        img_c_out = read_pgm(fn_saida_c)
        dif = img_py_out != img_c_out
        n_dif = np.sum(dif)
        total = img_py_out.size
        acc = 100.0 * (1 - n_dif/total)
        print(f"Diferenças encontradas: {n_dif}/{total}")
        print(f"Acurácia Python vs C: {acc:.2f}%")
        if n_dif > 0:
            coords = np.argwhere(dif)
            print("Exemplos de diferenças (até 10):")
            for (yy, xx) in coords[:10]:
                print(f"  Pixel[{yy},{xx}]: Python={img_py_out[yy,xx]} vs C={img_c_out[yy,xx]}")
    except Exception:
        pass
