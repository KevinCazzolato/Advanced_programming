// Cazzolato Kevin SM3201245
#ifndef MANDELBROT_H
#define MANDELBROT_H

struct _MandelBrotInfo {
    int IsInside;
    int IterMax;
};

typedef struct _MandelBrotInfo info;
typedef struct _MandelBrotInfo * info_ptr;

void computing(int* MandelbrotImage, int resolution, int maxIt);

void freeMandelbrotImage(int* mandelbrotImage);

int* allocateMandelbrotImage(int resolution, int ncols);

#endif // MANDELBROT_H
