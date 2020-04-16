CC=gcc
CFLAGS=-g -Wall -I. -lm
DEPS = Tree.h
OBJ = Tree.o Driver.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

driver: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)


.PHONY: clean

clean:
	rm -f ./*.o 
