#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <ctype.h>

#define WIDTH       89
#define HEIGHT      89
#define WINDOW_SIZE 55
#define K          -0.1 

/* Reflete coordenada x no intervalo [0..N-1] como faz o scipy.ndimage.uniform_filter(mode='reflect') */


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

void niblack(uint8_t in[HEIGHT][WIDTH], uint8_t out[HEIGHT][WIDTH]) {
    int w = WINDOW_SIZE / 2;

    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int x1 = (x - w < 0) ? 0 : x - w;
            int y1 = (y - w < 0) ? 0 : y - w;
            int x2 = (x + w >= WIDTH) ? WIDTH - 1 : x + w;
            int y2 = (y + w >= HEIGHT) ? HEIGHT - 1 : y + w;
            int area = (y2 - y1 + 1) * (x2 - x1 + 1);

            float sum = 0;
            float sum_sq = 0;

            for (int j = y1; j <= y2; j++) {
                for (int i = x1; i <= x2; i++) {
                    float val = in[j][i];
                    sum += val;
                    sum_sq += val * val;
                }
            }

            float mean = sum / area;
            float variance = (sum_sq - (sum * sum) / area) / (area - 1);
            if (variance < 0) variance = 0;
            float std = sqrtf(variance);
            float T = mean + K * std;

            out[y][x] = (in[y][x] < T) ? 0 : 255;
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
    niblack(img_in, img_out);
    write_pgm(argv[2], img_out);
    printf("Pronto: %s -> %s\n", argv[1], argv[2]);
    return 0;
}
