#bibliotecas utilizadas para leitura das imagens e exibição dos resultados
import numpy as np
import matplotlib.pyplot as plt

#função para leitura de imagens no formato PGM P2, respeitando comentários e cabeçalho
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

#código principal para comparar visualmente as saídas
if __name__ == "__main__":
    in_img  = read_pgm('test_input.pgm')   #imagem original
    out_c   = read_pgm('out_c.pgm')                           #saída em C
    out_py  = read_pgm('out_python_sk.pgm')                      #saída com Scikit-image
    out_cv  = read_pgm('out_python_cv.pgm')                      #saída com OpenCV

    plt.figure(figsize=(12, 4))  #ajusta o tamanho da figura para 4 imagens lado a lado

    # Imagem original
    plt.subplot(1, 4, 1)
    plt.title('Imagem de Entrada')
    plt.imshow(in_img, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')


    # Saída da implementação em C
    plt.subplot(1, 4, 2)
    plt.title('Saída em C')
    plt.imshow(out_c, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    # Saída da Scikit-image
    plt.subplot(1, 4, 3)
    plt.title('Scikit-image')
    plt.imshow(out_py, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    # Saída da OpenCV
    plt.subplot(1, 4, 4)
    plt.title('OpenCV')
    plt.imshow(out_cv, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')

    # salva o comparativo e exibe
    plt.tight_layout()
    plt.savefig('comparison_all.png', dpi=150)
    plt.show()
