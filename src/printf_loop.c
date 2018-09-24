#include <stdio.h>                                                                                                                                                                                           
#include <windows.h>                                                                                                                                                                                         
#include <process.h>                                                                                                                                                                                         

int main(void) {
	int i = 0;
	int pid = 0;
	pid = _getpid();
	while (1) {
		printf("[%d]Loop iteration %d!\n", pid, i);
		i++;
		Sleep(1 * 1000);
	}
}