/* gcc -pthread */
/* Show basic use of pthread and return value. */
#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
void * thread1(void *arg){
	printf("thread 1 returning\n");
	return ((void *)1);
}
void * thread2(void *arg){
	printf("thread 2 returning\n");
	pthread_exit((void *)2);
}

int main(void){
	int err;
	pthread_t tid1, tid2;
	void * tret;
	err = pthread_create(&tid1, NULL, thread1, NULL);
	err = pthread_create(&tid2, NULL, thread2, NULL);

	err = pthread_join(tid1, &tret);
	printf("thread 1 exit code %d \n", (int)tret);

	err = pthread_join(tid2, &tret);
	printf("thread 2 exit code %d \n", (int)tret);

	exit(0);
}
