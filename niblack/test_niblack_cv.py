#O objetivo geral desse código é a geração da limiarização segundo OpenCV e a comparação desta com a saída obtida no embarcado, por fim esta comparação é printada na forma de acuracia semelhança entre os pixels e, se houver divergencia, onde ela se encontra

#bibliotecas utilizadas para a geração da imagem binarizada segundo o OpenCV
import cv2
import numpy as np
from skimage.io import imread

#Dimensões da imagem escolhida pelo professor
WIDTH, HEIGHT = 89, 89
#tamanho da janela usada e constante da fórmula de Niblack
WINDOW_SIZE = 51
K = -0.1

#a variável image recebe a leitura da imagem de entrada e reafirmação do tipo para que a comparação seja efetiva utilizando o mesmo tipo
image = imread('test_input.pgm', as_gray=True)
if image.dtype != np.uint8:
    image = (image * 255).astype(np.uint8)

#image_f = image.astype(np.float32)

# Calcula a média local (janela deslizante) segundo o OpenCV com filtro de caixa
mean = cv2.boxFilter(image, ddepth=-1, ksize=(WINDOW_SIZE, WINDOW_SIZE), normalize=True)

# Calcula o desvio padrão local a partir da média dos quadrados e do quadrado da média
sqr = image * image
mean_sqr = cv2.boxFilter(sqr, ddepth=-1, ksize=(WINDOW_SIZE, WINDOW_SIZE), normalize=True)
std = np.sqrt(mean_sqr - mean**2)

# A variável thresh calcula o limiar da binarização segundo a fórmula de Niblack
# a variável binary armazena a binarização da imagem segundo esse limiar, convertendo para 0 e 255
thresh = mean + K * std
binary = (image> thresh).astype(np.uint8) * 255

#Abre e escreve o resultado da binarização com OpenCV no arquivo no formato .pgm P2
with open('out_python_cv.pgm', 'w') as f:
    f.write("P2\n")
    f.write("# Binarização Niblack com OpenCV\n")
    f.write(f"{WIDTH} {HEIGHT}\n")
    f.write("255\n")
    for row in binary:
        f.write(" ".join(str(pixel) for pixel in row) + "\n")
        
# A variável img_c armazena a leitura da saída que o código implementado deu para a mesma entrada e garante o mesmo tipo entre os pixels
img_c = imread('out_c.pgm', as_gray=True)
if img_c.dtype != np.uint8:
    img_c = (img_c * 255).astype(np.uint8)

# As imagens binárias são normalizadas para 0 e 1 para a comparação lógica
bin_py = (binary > 127).astype(np.uint8)
bin_c = (img_c > 127).astype(np.uint8)

# Inverte a lógica da imagem em C, assumindo que nela 0=texto e 255=fundo
bin_c_inv = 1 - bin_c

# Verifica as diferenças entre a imagem binarizada pelo OpenCV e pela implementação em C e armazena elas na variável diff
# A variável diff_map armazena essas diferenças onde elas existem de forma binarizada também
# A variável n_diff apresenta a soma de diferenças pontuais 
# A variável acc calcula a acurácia percentual
diff = (bin_py != bin_c_inv)
diff_map = (diff * 255).astype(np.uint8)
n_diff = np.sum(diff)
total = WIDTH * HEIGHT
acc = 100.0 * (1 - n_diff / total)

#Abre e escreve o resultado do mapa de diferenças no arquivo no formato .pgm P2
with open('mapa_diferencas.pgm', 'w') as f:
    f.write("P2\n")
    f.write("# Mapa de diferenças entre Python (OpenCV) e C\n")
    f.write(f"{WIDTH} {HEIGHT}\n")
    f.write("255\n")
    for row in diff_map:
        f.write(" ".join(str(pixel) for pixel in row) + "\n")

#Quando há diferenças, exibe uma a uma mostrando em que pixel se encontra e a diferença numérica entre a saída da implementação em C e a binarização em Python
if n_diff > 0:
    coords = np.argwhere(diff)
    print("Exemplos de diferenças:")
    for y, x in coords[:]:  
        print(f" Pixel[{y},{x}]: py={bin_py[y,x]} vs c_inv={bin_c_inv[y,x]}")

#Printa a diferença percentual
print(f"Diferenças: {n_diff}/{total} — Acurácia: {acc:.2f}%")
