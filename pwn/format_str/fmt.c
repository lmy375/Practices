#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define BUF_SIZE 256

char flag[]= "1 4m s3cr3t";
char s[] = "%s";
char x[] = "%x";
char d[] = "%d";

int main()
{
	char buf[BUF_SIZE];
	while(1){
		memset(buf,0,BUF_SIZE);
		read(STDIN_FILENO, buf, BUF_SIZE);
		printf(buf);
		fflush(stdout);
	}
	return 0;
}


