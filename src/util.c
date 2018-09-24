#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include "util.h"

int input_pid(void)
{
	char buf[32];
	long num;

	printf("pid: ");
	fgets(buf, sizeof(buf), stdin);

	num = atoi(buf);
	return num;
}

void show_error(void) {
	LPVOID lpMsgBuf;

	FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER |
		FORMAT_MESSAGE_FROM_SYSTEM |
		FORMAT_MESSAGE_IGNORE_INSERTS,
		NULL, GetLastError(),
		MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
		(LPTSTR)&lpMsgBuf, 0, NULL);

	/* MessageBox(NULL, (const char*)lpMsgBuf, NULL, MB_OK); */
	printf("%s", (const char*)lpMsgBuf);
	LocalFree(lpMsgBuf);
}
