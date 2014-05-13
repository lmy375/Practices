#include <stdio.h>
#include <windows.h>

#define THREAD_SUM 10
int tmp;
int sum;

DWORD WINAPI ThreadProc(LPVOID para){
	int i;
	for(i= 0;i<10000;i++)
		//InterlockedExchangeAdd(&tmp,1);
		tmp++;
	printf("%d ",(int)para);
	sum+=(int)para;
	return 0;
}

int main(){
	HANDLE hThread[THREAD_SUM];
	DWORD id;
	int i ;
	for(i= 0;i<THREAD_SUM;i++){
		hThread[i] = CreateThread(NULL,0,ThreadProc, i,0,&id);
	//	printf("%d ", id);
	}
	for(i=0;i<THREAD_SUM;i++){
		WaitForSingleObject(hThread[i],INFINITE);
	}	
	printf("\n%d\n%d", tmp, sum);
	return 0;
}