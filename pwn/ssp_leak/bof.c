// gcc bof.c -m32 -mpreferred-stack-boundary=2 -fstack-protector-all -o bof

#include <unistd.h>
#include <stdio.h>
char flag[]= "1 4m s3cr3t";

int main()
{
	char buf[4];
	read(STDIN_FILENO, buf, 256);
	return 0;
}
