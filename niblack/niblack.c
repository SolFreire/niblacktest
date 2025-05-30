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

static inline int min(int a, int b) { return a < b ? a : b; }
static inline int max(int a, int b) { return a > b ? a : b; }

void niblack(uint8_t in[HEIGHT][WIDTH], uint8_t out[HEIGHT][WIDTH]) {
    double integral[HEIGHT+1][WIDTH+1];
    double integral_sq[HEIGHT+1][WIDTH+1];

    for (int i = 0; i <= HEIGHT; i++) {
        integral[i][0] = 0;
        integral_sq[i][0] = 0;
    }
    for (int j = 0; j <= WIDTH; j++) {
        integral[0][j] = 0;
        integral_sq[0][j] = 0;
    }

    for (int y = 1; y <= HEIGHT; y++) {
        for (int x = 1; x <= WIDTH; x++) {
            double val = in[y-1][x-1];
            integral[y][x] = val + integral[y-1][x] + integral[y][x-1] - integral[y-1][x-1];
            integral_sq[y][x] = val*val + integral_sq[y-1][x] + integral_sq[y][x-1] - integral_sq[y-1][x-1];
        }
    }

    int w = WINDOW_SIZE / 2;
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            int x1 = max(x - w, 0);
            int y1 = max(y - w, 0);
            int x2 = min(x + w, WIDTH - 1);
            int y2 = min(y + w, HEIGHT - 1);

            int area = (y2 - y1 + 1) * (x2 - x1 + 1);

            int _x1 = x1;
            int _y1 = y1;
            int _x2 = x2 + 1;
            int _y2 = y2 + 1;

            double sum = integral[_y2][_x2] - integral[_y1][_x2] - integral[_y2][_x1] + integral[_y1][_x1];
            double sum_sq = integral_sq[_y2][_x2] - integral_sq[_y1][_x2] - integral_sq[_y2][_x1] + integral_sq[_y1][_x1];

            double mean = sum / area;
            double variance = (sum_sq - (sum*sum)/area) / (area - 1);

            if (variance < 0) variance = 0;
            
            double std = sqrt(variance);
            double T = mean + K * std;

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