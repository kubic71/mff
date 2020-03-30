#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{	
	char *m1="message1.";

	FILE *f=fopen("t1.dat", "a");
	fprintf(f,"%s",m1);
	exit(0);
} 

