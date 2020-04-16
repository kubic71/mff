#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Tree.h"
#include "Painter.h"

// char NPNtext[] = "* 150 s / x 20 "; // Example of NPN expression. Change it as you need
// char NPNtext[] = "159   "; // Example of NPN expression. Change it as you need


static void replace(char* str, char from, char to) {
	while (*str != '\0')
	{
		if(*str == from)
			*str = to;
		str++;
	}
	
}

static void plotTree(T_Tree tree) {
	byte* buffer;
	readFile("./Coordinates.bmp", &buffer);

	double y;

	double step = 0.1;
	double x = -399;

	while(x <= 399) {
		y = evaluateTree(tree, x);
		plot(x, y, buffer);
		x += step;
	}

	// All plots are saved here
	saveFile("plot.bmp", buffer);
}


int main(void) {

    char *line = NULL;

    size_t len = 0;
    int read = 0;
    while (read != -1) {
        printf("enter an expression:\n");
        read = getline(&line, &len, stdin);
		
        
		// to avoid edge-cases
		replace(line, '\n', ' ');
		replace(line, '\r', ' ');
		strcat(line, " ");

		int offset = 0;
		T_Tree t = parseTree(line, &offset);

		
		if(t != NULL) {
			if(line[offset] != '\0') {  
				printf("Invalid expression. Was able to parse only a part of it...\n");
			}
			displayTree(t);
			printf("\n");

			plotTree(t);

			destroyTree(t);
		} else
		{
			printf("Invalid expression!\n");
		}
		
    }
    free(line);

	return EXIT_SUCCESS;
}


