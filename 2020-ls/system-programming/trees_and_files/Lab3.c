#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "bst.h"
#include <stdbool.h>

/**
 * ask SIZE to the user, and create a binary file with random SIZE unsigned values.
 * Use srand(time(NULL)) at the beginning, and use rand()%SIZE to create a random number between 0
 * and SIZE-1
 */
void createFile(char* filename)
{
	int SIZE;
	printf("Enter file size:\n");
	scanf("%d", &SIZE);
	fflush(stdin);

	FILE *fout = fopen(filename, "wb");
	if (fout == NULL) {
		printf("Cannot open the file to write.");
		exit(-1);
	}

	srand(time(NULL));
	int r;
	for(int i=0; i< SIZE; i++) {
		r = rand() % SIZE;
		fwrite(&r, sizeof(r), 1, fout);
	}
	fclose(fout);

}
/**
 * Show the contents of the file in the screen (the list of unsigned values stored in the file)
 */
void showFile(char* filename)
{
	FILE *f = fopen(filename, "rb");
	int r;
	int count;
	
	while (true) {
		
		count = fread(&r, sizeof(r), 1, f);
		if (count == 0) break;
		printf("%d, ", r);
	}

	fclose(f);

}

/**
 * Store in the tree the values read from the file)
 */

void loadFile(char* filename, TTree* tree)
{
	FILE *fin = fopen(filename, "rb");
	int r;
	while(fread(&r, sizeof(r), 1, fin)) {
		insert(tree, r);
	}	
}


int main(void) {

	/* Create file with random positive integers */
	char fname[50];
	printf ("Enter the file name:\n");
	fflush(stdout);
	scanf ("%s",fname);
	fflush(stdin);
	createFile(fname);

	/* Read the created file */ 
	printf("\n Now, we read its contents and show them\n");
	showFile(fname);
	fflush(stdout);

	/* Load the file content into BST */
	printf ("\n Now, we load the content of the tree\n");
	TTree mytree;
	create (&mytree);
	loadFile(fname,&mytree);

	/* Print the BST in order */
	printf ("\n Now we show the ordered values in the tree\n");
	show(mytree);
	fflush(stdout);


	/* Replace the file with ordered values */
	printf("\n Now we write the ordered values\n");
	FILE * fd;
	fd = fopen (fname, "wb");
	save(mytree, fd);
	fclose (fd);
	printf("\n Finally, we show the ordered values in the file\n");
	showFile(fname);
	destroy (&mytree);

	return EXIT_SUCCESS;
}
