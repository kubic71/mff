CC=gcc
CFLAGS=-g -Wall -I. -lm
DEPS = Tree.h Painter.h
OBJ = Tree.o Driver.o Painter.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

driver: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)


.PHONY: clean

clean:
	rm -f ./*.o 
