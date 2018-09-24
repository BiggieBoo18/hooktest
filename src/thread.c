#include <stdio.h>
#include <windows.h>
#include <tlhelp32.h>
#include "thread.h"
#include "util.h"

int thread_list(int pid, PTHREADENTRY32 lpte) {
	int           i = 0;
	HANDLE        snapshot;
	THREADENTRY32 te;

	te.dwSize = sizeof(te);
	snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, pid);
	if (snapshot == INVALID_HANDLE_VALUE) {
		show_error();
		return (-1);
	}
	if (Thread32First(snapshot, &te)) {
		do {
			if (te.th32OwnerProcessID == pid) {
				/* printf("tid=%d\n", te.th32ThreadID); */
				lpte[i] = te;
				i++;
			}
		} while (Thread32Next(snapshot, &te));
	}
	return (i);
}

int set_thread_context(HANDLE h_thread, CONTEXT *ct) {
	SuspendThread(h_thread);
	if (!SetThreadContext(h_thread, *(&ct))) {
		show_error();
		return (1);
	}
	ResumeThread(h_thread);
	return (0);
}

int get_thread_context(HANDLE h_thread, CONTEXT *ct) {
	SuspendThread(h_thread);
	if (!GetThreadContext(h_thread, *(&ct))) {
		show_error();
		return (1);
	}
	/* printf("[Rip]0x%I64X\n", ct->Rip); */
	ResumeThread(h_thread);
	return (0);
}

int switch_TF(HANDLE h_thread) {
	CONTEXT ct;

	SuspendThread(h_thread);
	ct.ContextFlags = CONTEXT_FULL;
	if (!GetThreadContext(h_thread, &ct)) {
		show_error();
		return (1);
	}
	printf("[bEFlags]0x%lX\n", ct.EFlags);
	ct.EFlags ^= 0x00000100;
	printf("[aEFlags]0x%lX\n", ct.EFlags);
	if (set_thread_context(h_thread, &ct)) {
		return (1);
	}
	ResumeThread(h_thread);
	return (0);
}
