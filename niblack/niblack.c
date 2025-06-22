#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <ctype.h>

#define WIDTH       89
#define HEIGHT      89
#define WINDOW_SIZE 51
#define K          -0.1   

/* Reflete coordenada x no intervalo [0..N-1] como faz o scipy.ndimage.uniform_filter(mode='reflect') */
static inline int reflect(int x, int N) {
    if (x < 0)       return -x;
    else if (x >= N) return 2*N - 2 - x;
    else             return x;
}

void read_pgm(const char* filename, uint8_t img[HEIGHT][WIDTH]) {
    FILE* f = fopen(filename, "r");
    if (!f) { perror("fopen"); exit(1); }
    char magic[3];
    int w, h, maxv;
    if (fscanf(f, "%2s", magic) != 1 || strcmp(magic, "P2") != 0) {
        fprintf(stderr, "Arquivo não está em P2\n"); exit(1);
    }
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
    if (fscanf(f, "%d %d", &w, &h) != 2 || fscanf(f, "%d", &maxv) != 1) {
        fprintf(stderr, "Erro lendo cabeçalho\n"); exit(1);
    }
    if (w != WIDTH || h != HEIGHT || maxv != 255) {
        fprintf(stderr, "Dimensões inesperadas: %dx%d, maxv=%d\n", w, h, maxv);
        exit(1);
    }
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

void niblack_skimage(uint8_t in[HEIGHT][WIDTH], uint8_t out[HEIGHT][WIDTH]) {
    int w = WINDOW_SIZE / 2;
    int area = WINDOW_SIZE * WINDOW_SIZE;

    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            double sum = 0.0, sum_sq = 0.0;
            /* percorre toda janela WINDOW_SIZE x WINDOW_SIZE com reflect */
            for (int dy = -w; dy <= w; dy++) {
                int ry = reflect(y + dy, HEIGHT);
                for (int dx = -w; dx <= w; dx++) {
                    int rx = reflect(x + dx, WIDTH);
                    double v = in[ry][rx] / 255.0;
                    sum    += v;
                    sum_sq += v * v;
                }
            }
            double mean = sum / area;
            double var  = sum_sq / area - mean * mean;
            if (var < 0) var = 0;
            double std  = sqrt(var);
            double T    = mean + K * std;
            /* compara na escala [0,1] e depois dessatura de volta */
            double iv = in[y][x] / 255.0;
            out[y][x] = (iv > T) ? 255 : 0;
        }
    }
}

int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s entrada.pgm saida.pgm\n", argv[0]);
        return 1;
    }
    static uint8_t img_in[HEIGHT][WIDTH], img_out[HEIGHT][WIDTH];
    read_pgm(argv[1], img_in);
    niblack_skimage(img_in, img_out);
    write_pgm(argv[2], img_out);
    printf("Pronto: %s -> %s\n", argv[1], argv[2]);
    return 0;
}
