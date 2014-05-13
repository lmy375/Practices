#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

sigset_t chldmask;
sigset_t savemask;

int sign = 0;
void receive(int sig){
	printf("pid=%d, received\n", getpid());
	sign=1;
}
int main(){
	pid_t pid;

	sigemptyset(&chldmask);
	sigaddset(&chldmask, SIGUSR1);
	sigprocmask(SIG_BLOCK, &chldmask, &savemask);

	if((pid=fork())==0){
		signal(SIGUSR1, receive);
		sigprocmask(SIG_SETMASK, &savemask, NULL);
		while(sign==0);
		sign = 0;
		kill(getppid(), SIGUSR1);
		exit(0);
	}
	signal(SIGUSR1, receive);
	sigprocmask(SIG_SETMASK, &savemask, NULL);
	kill(pid, SIGUSR1);
	while(sign==0);
	sign =0;
}
