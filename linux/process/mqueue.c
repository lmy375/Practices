/*
   gcc -lrt -lm
   Calculate \sum^N_{i=1}{\sqrt{i}/{i+1}} using message queue.
*/
#include <stdio.h>
#include <errno.h>
#include <mqueue.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#define MY_MQ_P2C_NAME "/mymqP2cc"
#define MY_MQ_C2P_NAME "/mymqc2p"
#define MY_MQ_MAXMSG 10
#define MY_MQ_MSGSIZE 64

char msg_buf[MY_MQ_MSGSIZE];

pid_t createChild(mqd_t rmqdes, mqd_t smqdes){
	int recvValue;
	uint prio;
	pid_t pid = fork();
	float sum = 0;
	if(pid==0) {
		while(1){
				ssize_t msgSize = mq_receive(rmqdes, msg_buf, MY_MQ_MSGSIZE , &prio);
				if(msgSize <0){
					printf("child(%d):receive error:%s\n", getpid(), strerror(errno));
					exit(1);
				}
				memcpy((char*)&recvValue, msg_buf, msgSize);
				if(recvValue<0) break;
				sum+=sqrt(recvValue)/(recvValue+1);
		}
		memcpy(msg_buf, &sum , sizeof(float));
		int childPid = getpid();
		memcpy(msg_buf+sizeof(float), &childPid, sizeof(int));
		mq_send(smqdes, msg_buf, sizeof(float)+sizeof(int), 1);
	//	printf("child(%d):sum = %f\n", getpid(), sum);
		exit(0);
	}
	return pid;
}


int main(){
	pid_t childPid;
	int cpuNum = 1, waitStatus, i , exitMsg = -1;
	struct mq_attr attr;
	attr.mq_maxmsg = MY_MQ_MAXMSG;
	attr.mq_msgsize = MY_MQ_MSGSIZE;
	
	mqd_t p2cmqdes = mq_open(MY_MQ_P2C_NAME, O_RDWR|O_CREAT , 0664, &attr);
	mqd_t c2pmqdes = mq_open(MY_MQ_C2P_NAME, O_RDWR|O_CREAT , 0664, &attr);
	if(p2cmqdes<0|| c2pmqdes<0){
		printf("parent(%d):%s\n", getpid(), strerror(errno));
		return -1;
	}
	
	cpuNum = get_nprocs();	
	for(i=0 ;  i<cpuNum ; i++){
			childPid = createChild(p2cmqdes, c2pmqdes);
	}
	for(i=1;i<=1000000;i++){
			mq_send(p2cmqdes,(char*) &i , sizeof(int), 0);
	}
	for(i=0;i<cpuNum;i++){
			mq_send(p2cmqdes,(char*)&exitMsg, sizeof(int), 0);
	}
	float total = 0;
	for(i= 0;i<cpuNum ;i++){
			uint prio;
			mq_receive(c2pmqdes, msg_buf, MY_MQ_MSGSIZE, &prio);
			float sum ;
			int childPid;
			memcpy(&sum , msg_buf, sizeof(float));
			memcpy(&childPid, msg_buf+sizeof(float), sizeof(int));
			printf("child(%d):sum = %f\n", childPid, sum);
			total+=sum;
	}
	printf("Final result: %f\n", total);
	while((childPid= wait(&waitStatus))>0){
		printf("child %d exit\n", childPid);
	}
}
