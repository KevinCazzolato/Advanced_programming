// Cazzolato Kevin SM3201245
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include "pgm.h"


//salva l'immagine in formato PGM, in input riceve: il percorso del file, la matrice dei colori (calcolata in mandelbrot.c), la larghezza e la lunghezza,
//in output richiama la funzione close_image che si occupa di chiudere l'immagine
int Save_Pgm(char *path, int *matrix, int width, int height)
{
    netpbm image;
    int err = empty_image(path, width, height, &image); //verifica se è possibile aprire l'immagine (vedi fz sotto)
    if (err != 0) 
    {
        printf("Unable to open target image: %d\n", -err);
        return -5;
    }

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            char *c = pixel_at(&image, x, y); 
            int k=y*width;
            *c = matrix[k+x];
        }
    }

    return close_image(&image);
}

//funzione che serve ad "aprire" l'immagine in formato .pgm, in input riceve il percorso e la struttura netpbm_ptr
int open_image(char *path, netpbm_ptr img)
{
    img->fd = fopen(path, "r+"); //Apre il file specificato dal percorso path in modalità lettura/scrittura
    if (img->fd == NULL) // verifica se l'apertura ha avuto successo
    {
        return -2; // impossibile aprire il file
    }
    struct stat sbuf; //informazioni relativa all'immagine
    stat(path, &sbuf);
    img->size = sbuf.st_size;
    if (fscanf(img->fd, "P5\n%d %d\n255\n", &img->width, &img->height) != 2) //verifica se è nel formato corretto
    {
        fclose(img->fd);
        return -3; //l'immagine non è nel formato corretto
    }
    img->offset = ftell(img->fd);
    img->data = mmap((void *)0, img->size, PROT_READ | PROT_WRITE, MAP_SHARED, fileno(img->fd), 0); //mappa il contenuto dell'immagine in memoria con permessi di scrittura e lettura
    if (img->data == MAP_FAILED) // verifica se la mappatura ha avuto successo
    {
        fclose(img->fd);
        return -4; // impossibile mappare
    }
    return 0;
}


//la funzione ha lo scopo di creare un nuovo file di immagine nel formato Netpbm (.PGM) vuoto (tutti i pixel impostati a zero) con le dimensioni specificate
//in input riceve il percorso del file, la larghezza, l'altezza e la struttura netpbm_ptr
int empty_image(char *path, int width, int height, netpbm_ptr img)
{
    FILE *fd = fopen(path, "w+"); // Apre il file in modalità lettura con fopen
    if (fd == NULL) 
    {
        return -1;
    }
    fprintf(fd, "P5\n%d %d\n255\n", width, height); //scrive per la lettura in formato .PGM
    size_t dataSize = width * height;
    fseek(fd, dataSize - 1, SEEK_CUR);
    fputc(0, fd);
    fclose(fd);
    return open_image(path, img);
}

//calcola la posizione del pixel
char *pixel_at(netpbm_ptr img, int x, int y)
{
    if (img == NULL)
    {
        return NULL;
    }
    if (x < 0 || x >= img->width)
    {
        return NULL;
    }
    if (y < 0 || y >= img->height)
    {
        return NULL;
    }
    return &img->data[y * img->width + x + img->offset];
}

//chiude l'immagine e rimuove la mappatura del file
int close_image(netpbm_ptr img)
{
    if (img == NULL)
    {
        return -1;
    }
    munmap(img->data, img->size);
    fclose(img->fd);
    return 0;
}