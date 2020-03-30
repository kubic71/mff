#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

int main()
{	
	char *m1="message1.";

	int f=open("t2.dat", O_WRONLY|O_CREAT|O_APPEND, S_IRUSR|S_IWUSR );
	int c=0, d=1;
	d=d/c;
	write(f, m1, strlen(m1));
	return 0;
} 


