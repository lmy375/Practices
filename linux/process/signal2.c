#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>
void handler(int sig){
	if (sig==SIGTERM){
		printf("catch SIGTERM\n");
		exit(0);
	}
	else{
		printf("Signal %d\n", sig);
	}
}
int main(){
	pid_t pid;
	if((pid=fork())==0){
		signal(SIGTERM, handler);
		signal(SIGINT, handler);
		while(1) pause();
	}
	sleep(2);
	kill(pid, SIGINT);
	sleep(2);
	kill(pid, SIGTERM);
	return 0;
}
