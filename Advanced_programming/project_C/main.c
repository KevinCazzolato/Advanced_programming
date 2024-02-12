// Cazzolato Kevin SM3201245
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#include "mandelbrot.h"
#include "pgm.h"

int main(int argc, char *argv[]){

    //verifico che l'input abbia 4 argomenti: l'eseguibile, il nome dell'immagine, il numero max di iterazioni e la risoluzione verticale
    if (argc != 4) {
        fprintf(stderr, "The correct syntax is: %s <output_file.pgm> <max_iterations> <resolution>\n", argv[0]);
        exit(1); // altrimenti restiuisco l'errore e termino il programma
    }

    char *outputFileName = argv[1]; 
    int maxIterations = atoi(argv[2]); // converti in intero il formato in input (stringa) 
    int resolution = atoi(argv[3]);      
    int ncols = 1.5 * resolution;

    //double start = omp_get_wtime();

    int *mandelbrotImage = allocateMandelbrotImage(resolution, ncols);     //alloca memoria

    computing(mandelbrotImage , resolution, maxIterations); //calcola il frattale

    Save_Pgm("image.pgm", mandelbrotImage, ncols, resolution); //salva l'immagine

    freeMandelbrotImage(mandelbrotImage); //libera la memoria

    //double end = omp_get_wtime();
    //double t=(end-start);

    //printf("Tempo impiegato: %f s\n ", t);

    return 0;
}
