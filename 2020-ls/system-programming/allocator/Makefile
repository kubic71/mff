CC=gcc
CFLAGS=-I.
DEPS = MemoryManager.h
OBJ = LabConcurrency01.o MemoryManager.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

allocator: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)


.PHONY: clean

clean:
	rm -f ./*.o 
