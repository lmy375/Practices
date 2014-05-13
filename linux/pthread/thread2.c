/*
   Show basic use of mutex lock.
*/
#include <pthread.h>
#include <stdio.h>

#define N 100000
//volatile int cnt = 0;
int cnt;
pthread_mutex_t mutex;
void *thread(void *arg){
	int i;
	for(i=0;i<N;i++){
			pthread_mutex_lock(&mutex);
			cnt++;
			pthread_mutex_unlock(&mutex);
	}
	return 0;
}


int main(){
	pthread_t tid1, tid2;
	pthread_mutex_init(&mutex, NULL);

	pthread_create(&tid1, NULL, thread, NULL);
	pthread_create(&tid2, NULL, thread, NULL);

	pthread_join(tid1 , NULL);
	pthread_join(tid2 , NULL);

	printf("cnt = %d\n", cnt);
	return 0;
}
