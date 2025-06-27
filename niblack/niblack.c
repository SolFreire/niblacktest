/*O objetivo geral desse código é a geração da limiarização segundo o método de Niblack implementado em linguagem C, e a escrita do resultado final no formato PGM P2, com estrutura compatível para comparação com a saída do algoritmo em Python e com método principal fielmente ao implementado no stm */

/*bibliotecas utilizadas para leitura, escrita, operações matemáticas e manipulação de strings*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <ctype.h>

/*Dimensões da imagem escolhida pelo professor*/
#define WIDTH       89
#define HEIGHT      89

/*Tamanho da janela usada e constante da fórmula de Niblack*/
#define WINDOW_SIZE 51
#define K          -0.1

/*Função para ler o arquivo no formato pgm P2 considerando sua estrutura
  Os dados são armazenados na variável 'img', que será processada pela função de limiarização*/
void read_pgm(const char* filename, uint8_t img[HEIGHT][WIDTH]) {
    FILE* f = fopen(filename, "r");
    if (!f) { perror("fopen"); exit(1); }

    char magic[3];
    int w, h, maxv;

    // Lê o cabeçalho do arquivo e valida o formato
    if (fscanf(f, "%2s", magic) != 1 || strcmp(magic, "P2") != 0) {
        fprintf(stderr, "Arquivo não está em P2\n");
        exit(1);
    }

    // Ignora comentários no cabeçalho
    int ch;
    while ((ch = fgetc(f)) != EOF) {
        if (ch == '#') {
            while ((ch = fgetc(f)) != '\n' && ch != EOF);
        } else if (isspace(ch)) {
            continue;
        } else {
            ungetc(ch, f);
            break;
        }
    }

    // Lê dimensões e valor máximo de intensidade
    if (fscanf(f, "%d %d", &w, &h) != 2 || fscanf(f, "%d", &maxv) != 1) {
        fprintf(stderr, "Erro lendo cabeçalho\n");
        exit(1);
    }

    // Valida se as dimensões são compatíveis com o esperado
    if (w != WIDTH || h != HEIGHT || maxv != 255) {
        fprintf(stderr, "Dimensões inesperadas: %dx%d, maxv=%d\n", w, h, maxv);
        exit(1);
    }

    // Lê os valores dos pixels para a matriz img
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int v;
            if (fscanf(f, "%d", &v) != 1) {
                fprintf(stderr, "Erro lendo pixel [%d,%d]\n", y, x);
                exit(1);
            }
            img[y][x] = (uint8_t)v;
        }
    }

    fclose(f);
}

/*Função para escrever a imagem resultante da binarização no formato PGM P2
  A matriz 'img' é a imagem binarizada, já processada pelo método de Niblack*/
void write_pgm(const char* filename, uint8_t img[HEIGHT][WIDTH]) {
    FILE* f = fopen(filename, "w");
    if (!f) { perror("fopen"); exit(1); }

    fprintf(f, "P2\n# Niblack (match skimage)\n%d %d\n255\n", WIDTH, HEIGHT);
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            fprintf(f, "%d ", img[y][x]);
        }
        fprintf(f, "\n");
    }

    fclose(f);
}

/*Função de limiarização segundo Niblack:
  Recebe como entrada a imagem original 'in', e como saída 'out' que será binarizada.
  Para cada pixel, é calculada a média e o desvio padrão da vizinhança local definida por WINDOW_SIZE*/
void niblack(uint8_t in[HEIGHT][WIDTH], uint8_t out[HEIGHT][WIDTH]) {
    int w = WINDOW_SIZE / 2;

    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            // Define limites da janela local, respeitando bordas
            int x1 = (x - w < 0) ? 0 : x - w;
            int y1 = (y - w < 0) ? 0 : y - w;
            int x2 = (x + w >= WIDTH) ? WIDTH - 1 : x + w;
            int y2 = (y + w >= HEIGHT) ? HEIGHT - 1 : y + w;
            int area = (y2 - y1 + 1) * (x2 - x1 + 1);

            float sum = 0;
            float sum_sq = 0;

            // Calcula soma e soma dos quadrados na janela
            for (int j = y1; j <= y2; j++) {
                for (int i = x1; i <= x2; i++) {
                    float val = in[j][i];
                    sum += val;
                    sum_sq += val * val;
                }
            }

            // Cálculo da média e do desvio padrão local
            float mean = sum / area;
            float variance = (sum_sq - (sum * sum) / area) / (area - 1);
            if (variance < 0) variance = 0;
            float std = sqrtf(variance);

            // Cálculo do limiar de Niblack
            float T = mean + K * std;

            // Binarização: se o pixel for menor que o limiar, é 0 (preto), senão 255 (branco)
            out[y][x] = (in[y][x] < T) ? 0 : 255;
        }
    }
}

/*Função principal do programa:
  Espera dois argumentos: nome do arquivo de entrada e de saída.
  Lê a imagem de entrada, aplica o método de Niblack e escreve o resultado.*/
int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s entrada.pgm saida.pgm\n", argv[0]);
        return 1;
    }

    // Declaração das matrizes de entrada e saída
    static uint8_t img_in[HEIGHT][WIDTH], img_out[HEIGHT][WIDTH];

    // Leitura, processamento e escrita
    read_pgm(argv[1], img_in);
    niblack(img_in, img_out);
    write_pgm(argv[2], img_out);

    // Confirmação da execução
    printf("Pronto: %s -> %s\n", argv[1], argv[2]);
    return 0;
}
