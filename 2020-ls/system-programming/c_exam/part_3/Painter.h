/*
 * Painter.h
 *
 *  Created on: 5 abr. 2020
 *      Author: galvez
 */

#ifndef PAINTER_H_
#define PAINTER_H_

typedef unsigned char byte;

#define SIZE 40062 // the size of the template image

// Reads a bitmap monochrome image file into memory
void readFile(char * fileName, byte** buffer);
/*
 * Sets to black (0) a bit in the image previously loaded into memory.
 * The value of x must be in the range -399 to 399.
 * The value of y must be in the range -199 to 199.
 * If x or y are not in these ranges, this function does nothing.
 * The coordinates (x,y) must be translated into coordinates of the image
 * corresponding to a particular bit in a particular byte.
 */
void plot(double x, double y, byte* buffer);
// Saves a previously loaded bitmap monochrome image into a file
void saveFile(char *fileName, byte* buffer);

#endif /* PAINTER_H_ */
