#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

int main()
{	
	char *m1="message1.";
	char *m2="message2.";

	int f=open("t2.dat", O_WRONLY|O_CREAT|O_APPEND, S_IRUSR|S_IWUSR );
	write(f, m1, strlen(m1));
	int pid=fork();
	if (pid==0)
	{
		write(f, m2, strlen(m2));
		exit(0);
	}
	return 0;
} 

