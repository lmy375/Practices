#include <signal.h>
#include <stdio.h>
void handler(int sig){
	static int beeps = 0;
	printf("BEEP\n");
	if(++beeps< 5)
		alarm(1);
	else{
		printf("BOOM!\n");
		exit(0);
	}
}
int main(){
	signal(SIGALRM, handler);
	alarm(5);

	while(1){;}
	exit(0);
}
