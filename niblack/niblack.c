#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <ctype.h>

#define WIDTH  89
#define HEIGHT 89
#define WINDOW_SIZE 15   
#define K -0.2         

void read_pgm(const char* filename, uint8_t img[HEIGHT][WIDTH]) {
    FILE* f = fopen(filename, "r");
    if (!f) { perror("fopen"); exit(1); }
    char magic[3];
    int w, h, maxv;
    if (fscanf(f, "%2s", magic) != 1 || strcmp(magic, "P2") != 0) {
        fprintf(stderr,"Arquivo não está em P2\n"); exit(1);
    }
    int ch;
    while (1) {
        ch = fgetc(f);
        if (ch == '#') {
            while ((ch = fgetc(f)) != '\n' && ch != EOF);
        } else if (isspace(ch)) {
            continue;
        } else {
            ungetc(ch, f);
            break;
        }
    }
    if (fscanf(f, "%d %d", &w, &h) != 2) {
        fprintf(stderr,"Falha ao ler dimensões\n"); exit(1);
    }
    if (fscanf(f, "%d", &maxv) != 1) {
        fprintf(stderr,"Falha ao ler valor máximo\n"); exit(1);
    }
    if (w != WIDTH || h != HEIGHT || maxv != 255) {
        fprintf(stderr, "PGM não atende dimensões esperadas: %dx%d, maxv=%d\n", w, h, maxv);
        exit(1);
    }
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int v;
            if (fscanf(f, "%d", &v) != 1) {
                fprintf(stderr,"Erro lendo pixel [%d,%d]\n", y, x);
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
    fprintf(f, "P2\n# Niblack binarization\n%d %d\n255\n", WIDTH, HEIGHT);
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            fprintf(f, "%d ", img[y][x]);
        }
        fprintf(f, "\n");
    }
    fclose(f);
}

static inline int clamp(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

void niblack(uint8_t in[HEIGHT][WIDTH], uint8_t out[HEIGHT][WIDTH]) {
    int w = WINDOW_SIZE / 2;
    int N = WINDOW_SIZE * WINDOW_SIZE;
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            double sum = 0, sum2 = 0;
            for (int dy = -w; dy <= w; dy++) {
                for (int dx = -w; dx <= w; dx++) {
                    int yy = clamp(y + dy, 0, HEIGHT - 1);
                    int xx = clamp(x + dx, 0, WIDTH - 1);
                    double v = in[yy][xx];
                    sum += v;
                    sum2 += v * v;
                }
            }
            double mean = sum / N;
            double var = (sum2 - N * mean * mean) / (N - 1);
            double std = sqrt(var);
            double T = mean + K * std;
            out[y][x] = (in[y][x] < T ? 0 : 255);
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
