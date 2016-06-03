// gcc bof.c -fno-stack-protector -o bof_64
// gcc bof.c -m32 -mpreferred-stack-boundary=2 -fno-stack-protector -o bof_32
#include <unistd.h>
#include <stdio.h>
int main()
{
	char buf[4];
	setbuf(stdin,0);
	setbuf(stdout,0);
	setbuf(stderr,0);

	read(STDIN_FILENO, buf, 256);
	write(STDOUT_FILENO,buf, 4);
	return 0;

}
