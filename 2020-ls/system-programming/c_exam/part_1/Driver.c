#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Tree.h"

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


int main(void) {

    char *line = NULL;
    size_t len = 0;
    int read = 0;
    while (read != -1) {
        puts("enter an expression:\n");
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
			destroyTree(t);
		} else
		{
			printf("Invalid expression!\n");
		}
		
    }
    free(line);

	return EXIT_SUCCESS;
}


