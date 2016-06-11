#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX 256

char flag[] = "this is flag~~~";
char name[MAX];
void * heaps[MAX];

void new_heap()
{
	int index = 0, size = 0;
	puts("input index:");
	scanf("%d", &index);
	puts("input size:");
	scanf("%d", &size);
	heaps[index] = malloc(size);
}

void edit_heap()
{
	int index = 0, size = 0;
	puts("input index:");
	scanf("%d", &index);
	puts("input size:");
	scanf("%d", &size);
	puts("input content:");
	// heap overflow here.
	read(STDIN_FILENO, heaps[index], size);
}

void print_heap()
{
	int index = 0, size = 0;
	puts("input index:");
	scanf("%d", &index);
	puts("input size:");
	scanf("%d", &size);
	write(STDOUT_FILENO, heaps[index], size);
}

void free_heap()
{
	int index = 0;
	puts("input index:");
	scanf("%d", &index);
	free(heaps[index]);
}

void input_name()
{
	puts("input name:");
	read(STDIN_FILENO, name, MAX);
}

int main()
{
	int option;
	setbuf(stdin, 0);
	setbuf(stdout,0);
	setbuf(stderr,0);
	while(1){
		puts("1 - new\n2 - edit\n3 - print\n4 - free\n5 - name\n6 - exit\ninput:");
		scanf("%d", &option);
		switch(option){
			case 1: new_heap(); break;
			case 2: edit_heap(); break;
			case 3: print_heap(); break;
			case 4: free_heap(); break;
			case 5: input_name(); break;
			case 6: exit(0); break;
			default: puts("error!\n");
		}
	}
}
