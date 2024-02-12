// Cazzolato Kevin SM3201245
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <omp.h>
#include <math.h>
#include "mandelbrot.h"

//funzione per allocare la memoria 
int* allocateMandelbrotImage(int resolution, int ncols) {
    int* image = (int*)malloc(resolution * ncols * sizeof(int));
    return image;
}

// Funzione per liberare la memoria allocata per l'immagine Mandelbrot
void freeMandelbrotImage(int* mandelbrotImage) {
    free(mandelbrotImage);
}

// Funzione per calcolare l'insieme di Mandelbrot: in input riceve l'allocazione della memoria per l'immagine, la risoluzione è il numero di iterazioni massime.
// La funzione calcola l'appartenenza o meno dei punti all'insieme di Mandelbrot e in output non restituisce niente, in quanto agisce unicamente su un puntatore,
// dunque non è necessario restituire nulla.
void computing(int* MandelbrotImage, int resolution, int maxIt) {
    int k;
    int ncols=resolution*1.5;
    if(resolution %2==0){
        k=resolution/2;
    }else{
        k= (resolution/2)+1;
    }
    if (resolution<0){
        printf("impossibile generare un immagine con una risoluzione negativa \n");
        exit(2);
    }
    // mis pred rate = 0.9% => lascio la possibilità di fare branch
    #pragma omp parallel for collapse(2)
    for (int x = 0; x < k; x++) { 
        for (int y = 0; y < ncols; y++) {
            struct _MandelBrotInfo info;
            info.IsInside = 1;

            double real = -2.0 + (3.0 * y) / (1.5 * resolution);
            double im = -1.0 + (2.0 * x) / resolution;
            double complex c = real + im * I;
            double complex z = 0.0 + 0.0 * I;

            for (int iter = 0; iter < maxIt; iter++) {
                z = z * z + c;
                if (cabs(z) > 2.0) { //lascio la possibilità di branch poichè sbaglierò il predict al più una volta
                    info.IsInside = 0;
                    info.IterMax = iter;
                    break;
                }
            }
            //Lascio la possibilità di fare branch in quanto non inficia di molto sull'efficienza del programma. Inoltre, si è visto empiricamente che 
            //i tempi di esecuzione nella versione con i branch, diminuiscono, anche se in minima parte. Infine il missing predict rate dell'intero programma 
            // è di 0.9%, dunque molto basso.
            if (info.IsInside == 1) {
                MandelbrotImage[x * ncols + y] = 255;
                MandelbrotImage[(resolution - x - 1) * ncols + y] = 255; //per simmetria della fz
            } else {
                MandelbrotImage[x * ncols + y] = 255 * log(info.IterMax + 1.0) / log(maxIt);
                MandelbrotImage[(resolution - x - 1) * ncols + y] = 255 * log(info.IterMax + 1.0) / log(maxIt);
            }
            
        }
    }
}