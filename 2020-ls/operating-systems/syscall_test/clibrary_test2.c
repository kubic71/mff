#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{	
	char *m1="message1.";
	char *m2="message2.";

	FILE *f=fopen("t1.dat", "a");
	fprintf(f,m1);
	int pid=fork();
	if (pid==0)
	{
		fprintf(f,m2);
	}
	exit(0);
} 

