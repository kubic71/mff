#include "Painter.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Reads a bitmap monochrome image file into memory
void readFile(char * fileName, byte** buffer) {
	FILE *in = fopen(fileName, "rb");
	fseek(in, 0, SEEK_END); // Seek to end of file
	int size = ftell(in);	// Get current file pointer
	fseek(in, 0, SEEK_SET);

	printf("SIZE: %d\n", size); //debug

	*buffer = (byte *)malloc(size);
	fread(*buffer, 1, size, in);
	fclose(in);
}

void plot(double xd, double yd, byte* bmp_buffer) {
	int x = xd + 399;
	int y = yd + 199;

	if(x < 0 || x >= 799  || y < 0 || y >= 399) {
		// printf("x: %f y:%f not in range\n", x, y);
		return;
	}

	
	/*
 * Sets to black (0) a bit in the image previously loaded into memory.
 * The value of x must be in the range -399 to 399.
 * The value of y must be in the range -199 to 199.
 * If x or y are not in these ranges, this function does nothing.
 * The coordinates (x,y) must be translated into coordinates of the image
 * corresponding to a particular bit in a particular byte.
 */

	int byte_n = y*100 + x/8;
	int bit_n =  x % 8;
	int offset = 14 + (bmp_buffer[15] << 8) + bmp_buffer[14] + 8;
	bmp_buffer[offset + byte_n] = bmp_buffer[offset + byte_n] & (~(0b10000000 >> bit_n));

}

// Saves a previously loaded bitmap monochrome image into a file

void saveFile(char *fileName, byte* buffer) {
	// Save the resulting file
	FILE *out = fopen("./plot.bmp", "wb");
	fwrite(buffer, 1, SIZE, out);
	fclose(out);
}