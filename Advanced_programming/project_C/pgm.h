// Cazzolato Kevin SM3201245
#ifndef PGM_H
#define PGM_H
#include <stdio.h>

struct _netpbm_image {
  int width;
  int height;
  int offset;
  int size;
  FILE * fd;
  char * data;
};

typedef struct _netpbm_image netpbm;
typedef struct _netpbm_image * netpbm_ptr;

int Save_Pgm(char *path, int *matrix, int width, int height);

int open_image(char *path, netpbm_ptr img);

int empty_image(char *path, int width, int height, netpbm_ptr img);

char *pixel_at(netpbm_ptr img, int x, int y);

int close_image(netpbm_ptr img);

#endif // PGM_H
