#include <stdio.h>

int main(){
	int i = 0;
	int tmp = 0;
	srand(0);
	while (i<200){
		srand(rand());
		printf("%d\n", rand()%99999+1);
		i++;
	}
	return 0;
}
