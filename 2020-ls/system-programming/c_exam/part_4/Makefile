CC=gcc
CFLAGS=-g -Wall -I. -lm
DEPS = Tree.h Painter.h List.h
OBJ = Tree.o Driver.o Painter.o List.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

driver: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)


.PHONY: clean

clean:
	rm -f ./*.o 
