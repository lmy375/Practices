/* Signal of thread.*/

#include <pthread.h>
#include <stdio.h>
#include <signal.h>

void *sig_thread(void *arg){
		sigset_t * set = (sigset_t *)arg;
		int s, sig;
		for(;;){
				sigwait(set, &sig);
				printf("Signal handling thread got signal %d\n", sig);
		}
}

int main(){
		pthread_t thread;
		sigset_t set;

		sigemptyset(&set);
		sigaddset(&set, SIGQUIT);
		sigaddset(&set, SIGUSR1);
		pthread_sigmask(SIG_BLOCK, &set, NULL);

		pthread_create(&thread, NULL, &sig_thread, (void*)&set);
		sleep(1);
		kill(getpid(), SIGUSR1);
		kill(getpid(), SIGQUIT);
		pause();
		return 0;
}
