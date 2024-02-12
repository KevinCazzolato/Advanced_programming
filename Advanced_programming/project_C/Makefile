#Cazzolato Kevin SM3201245
CC = gcc
CFLAGS = -O3 -fopenmp -march=native -std=c17 -Wall -pedantic -funroll-loops 
HEADERS = $(wildcard *.h)
SOURCES = $(wildcard *.c)
OBJECTS = $(SOURCES:.c=.o) 
EXECUTABLE = main

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ -lm

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $<

.PHONY: clean

clean:
	rm -f *.o *.pgm

