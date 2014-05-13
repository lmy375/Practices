/*
	Use of condition.
*/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
pthread_cond_t cond;
pthread_mutex_t mutex;
int count;
void * wait_thread(){
	pthread_mutex_init(&mutex,NULL);
	while(count<=0){
			printf("wait thread starts to wait. count=%d\n", count);
			pthread_cond_wait(&cond, &mutex);
			printf("wait thread continues. count=%d\n", count);
	}
	pthread_mutex_unlock(&mutex);
	printf("wait thread ends. count=%d\n", count);
}
void * unlock_thread(){
	pthread_mutex_init(&mutex,NULL);
	printf("unlock thread get the lock. count=%d\n", count);
	++count;
	printf("unlock thread increase the counter. count=%d\n", count);
	pthread_cond_signal(&cond);
	printf("unlock thread send signal\n");
	pthread_mutex_unlock(&mutex);
	printf("unlock thread ends\n");
}
int main(){
		pthread_t tid1, tid2;

		pthread_cond_init(&cond,NULL);

		pthread_create(&tid1, NULL, wait_thread, NULL);
		sleep(2);
		pthread_create(&tid2, NULL, unlock_thread, NULL);

		pthread_join(tid1, NULL);
		pthread_join(tid2, NULL);

		pthread_cond_destroy(&cond);

		return 0;
}


		

