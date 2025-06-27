#O objetivo geral desse código é a geração da limiarização segundo skimage e a comparação desta com a saída obtida no embarcado, por fim esta comparação é printada na forma de acuracia  semelhança entre os pixels e, se houver divergencia, onde ela se encontra


#bibliotecas utilizadas para a geração da imagem binarizada segundo o scikitlearn
import numpy as np
from skimage import io, filters
from skimage.io import imread, imsave

#Dimensões da imagem escolhida pelo professor
WIDTH, HEIGHT = 89, 89
#tamanho da janela iusada e constante da formula de niblack
WINDOW_SIZE = 51
K = -0.1

#a variável imagem recebe a leitura da imagem de entrada e reafirmação do tipo para que a comparação seja efetiva utilizando o mesmo tipo
image = imread('test_input.pgm', as_gray=True)
if image.dtype != np.uint8:
    image = (image * 255).astype(np.uint8)

# Calcula o threshold adaptativo com Niblack segundo skimage na mesma escala e tipo da imagem lida no c (uint8)
# A variável thresh calcula o limiar da binarização segundo a implementação d biblioteca sk
# a biblioteca binary_sk recebe a binarização da imagem segundo o limiar do método da sk
thresh = filters.threshold_niblack(image, window_size=WINDOW_SIZE, k=K)
binary_sk = (image > thresh).astype(np.uint8) * 255


#Abre e escreve um resultado no arquivo no formato .pgm P2
with open('out_python_sk.pgm', 'w') as f:
    f.write("P2\n")
    f.write("# Binarização Niblack em Python\n")
    f.write(f"{WIDTH} {HEIGHT}\n")
    f.write("255\n")
    for row in binary_sk:
        f.write(" ".join(str(pixel) for pixel in row) + "\n")

# A variável img_c armazena a leitura da saída que o código implementado deu para a mesma entrada e garante o mesmo tipo entre os pixels
img_c = imread('out_c.pgm', as_gray=True)
if img_c.dtype != np.uint8:
    img_c = (img_c * 255).astype(np.uint8)

bin_py = (binary_sk > 127).astype(np.uint8)
bin_c = (img_c > 127).astype(np.uint8)
bin_c_inv = 1 - bin_c

# Verifica as diferenças entre a imagem binarizada pelo sk e pela implementação em c e armazena elas na variável diff
# A variável difmap armazena essas diferenças onde elas existem de forma binarizada também
# A variável n_diff apresenta a soma de diferenças pontuais 
# A Variável acc calcula a acurácia percentual
diff = (binary_sk != img_c)
diff_map = (diff * 255).astype(np.uint8)
n_diff = np.sum(diff)
total = WIDTH * HEIGHT
acc = 100.0 * (1 - n_diff / total)


#Abre e escreve um resultado o mapa de diferenças no arquivo no formato .pgm P2
with open('mapa_diferencas.pgm', 'w') as f:
    f.write("P2\n")
    f.write("# Mapa de diferenças entre Python e C\n")
    f.write(f"{WIDTH} {HEIGHT}\n")
    f.write("255\n")
    for row in diff_map:
        f.write(" ".join(str(pixel) for pixel in row) + "\n")

#Quando há diferenças, exibe uma a uma mostrando em que pixel se encontra e a diferença numérica entre a saída da implementação em c e a segundo a sk
if n_diff > 0:
    coords = np.argwhere(diff)
    print("Exemplos de diferenças:")
    for y, x in coords[:]:  
        print(f" Pixel[{y},{x}]: sk={binary_sk[y,x]} vs c={img_c[y,x]}")

#Printa a diferença
print(f"Diferenças: {n_diff}/{total} — Acurácia: {acc:.2f}%")
