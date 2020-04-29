CC=gcc
CFLAGS=-g -Wall -I.
DEPS = bst.h
OBJ = bst.o Lab3.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

all: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)


.PHONY: clean

clean:
	rm -f ./*.o 
