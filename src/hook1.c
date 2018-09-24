#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>
#include <tlhelp32.h>
#include "memory.h"
#include "module.h"
#include "privilege.h"
#include "thread.h"
#include "util.h"

int usage(char *command) {
	puts("usage");
	printf("%s <dll name> <function name>\n", command);

	return (0);
}

int hook(HANDLE h_process, HANDLE h_thread) {
	CONTEXT ct;
	SIZE_T  count = 0;

	ct.ContextFlags = CONTEXT_FULL;
	get_thread_context(h_thread, &ct);
	printf("Rsp=0x%016llX\n", ct.Rsp);
	// char   buf[BUF_SIZE] = { 0x09 };
	int   buf = rand();
	count = write_process_memory(h_process, (LPVOID)(ct.Rsp + 0x1BF8), &buf, sizeof(buf));
	//count = write_process_memory(h_process, (LPVOID)(ct.Rsp + 0x268), &buf, sizeof(buf));
	if (!count) {
		return (1);
	}
	printf("count=%zd\n", count);
	input_pid(); // for debug
	return (0);
}

int main(int argc, char *argv[]) {
	int         pid = -1;
	int         first_break = 0;
	int         quit = 0;
	int         dwStatus = 0;
	int         ret = 0;
	HANDLE      h_process;
	HANDLE      h_thread;
	FARPROC     address;
	DEBUG_EVENT de;
	char        orig_byte[BUF_SIZE] = {0};
	char        read_buf[BUF_SIZE] = {0};
	SIZE_T      count = 0;
	DWORD       tid = 0;


	//printf("BEFORE\n");
	//show_privileges();
	ret = set_debug_privilege("seDebugPrivilege");
	if (ret) {
		//printf("ret=%d\n", ret);
		show_error();
		return (1);
	}
	//printf("AFTER\n");
	//show_privileges();

	// check arguments
	if (argc <= 3) {
		usage(argv[0]);
		return (1);
	}

	srand((unsigned)time(NULL));

	pid = input_pid();
	h_process = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid); // get process handle
	if (!h_process) {
		show_error();
		return (1);
	}
	if (!DebugActiveProcess(pid)) { // attach
		CloseHandle(h_process);
		show_error();
		return (1);
	}
	/* printf("attached\n"); */
	// address = module_address("ucrtbased.dll", "__stdio_common_vfprintf");
	address = module_address("KERNEL32.DLL", "WriteFile");
	if (!address) {
		return (1);
	}
	count = read_process_memory(h_process, address, &orig_byte, sizeof(orig_byte));
	if (!count) {
		return (1);
	}
	if (set_sw_bp(h_process, address, &read_buf)) {
		return (1);
	}
	for (;;) {
		if (!WaitForDebugEvent(&de, INFINITE)) {
			break;
		}
		dwStatus = DBG_EXCEPTION_NOT_HANDLED;
		printf("%d\n", de.dwDebugEventCode);
		switch (de.dwDebugEventCode) {
		case EXCEPTION_DEBUG_EVENT:
			/* printf("  %d\n", de.u.Exception.ExceptionRecord.ExceptionCode); */
			switch (de.u.Exception.ExceptionRecord.ExceptionCode) {
			case EXCEPTION_BREAKPOINT:
				if (!first_break) {
					first_break = 1;
				}
				else {
					//printf("%d==%d\n", de.dwProcessId, pid);
					if (de.dwProcessId == pid) {
						//puts("here1");
						h_thread = OpenThread(THREAD_ALL_ACCESS, FALSE, de.dwThreadId);
						if (!h_thread) {
							show_error();
							return (1);
						}
						tid = de.dwThreadId;
						hook(h_process, h_thread);
						if (sw_bp_post_proc(h_process, h_thread, address, &orig_byte)) {
							return (1);
						}
						if (switch_TF(h_thread)) {
							return (1);
						}
						dwStatus = DBG_CONTINUE;
						CloseHandle(h_thread);
						//quit = 1;
					}
				}
				break;
			case EXCEPTION_SINGLE_STEP:
				//printf("%d==%d\n", de.dwProcessId, pid);
				if (de.dwProcessId == pid) {
					//puts("here2");
					h_thread = OpenThread(THREAD_ALL_ACCESS, FALSE, de.dwThreadId);
					if (!h_thread) {
						show_error();
						return (1);
					}
					tid = de.dwThreadId;
					set_sw_bp(h_process, address, &read_buf);
					/* switch_TF(h_thread); */
					dwStatus = DBG_CONTINUE;
					CloseHandle(h_thread);
					//quit = 1;
				}
				break;
			case EXCEPTION_ACCESS_VIOLATION:
				printf("EXCEPTION_ACCESS_VIOLATION\n");
				break;
			case EXCEPTION_DATATYPE_MISALIGNMENT:
				printf("EXCEPTION_DATATYPE_MISALIGNMENT\n");
				break;
			case EXCEPTION_ARRAY_BOUNDS_EXCEEDED:
				printf("EXCEPTION_ARRAY_BOUNDS_EXCEEDED\n");
				break;
			case EXCEPTION_FLT_DENORMAL_OPERAND:
				printf("EXCEPTION_FLT_DENORMAL_OPERAND\n");
				break;
			case EXCEPTION_FLT_DIVIDE_BY_ZERO:
				printf("EXCEPTION_FLT_DIVIDE_BY_ZERO\n");
				break;
			case EXCEPTION_FLT_INEXACT_RESULT:
				printf("EXCEPTION_FLT_INEXACT_RESULT\n");
				break;
			case EXCEPTION_FLT_INVALID_OPERATION:
				printf("EXCEPTION_FLT_INVALID_OPERATION\n");
				break;
			case EXCEPTION_FLT_OVERFLOW:
				printf("EXCEPTION_FLT_OVERFLOW\n");
				break;
			case EXCEPTION_FLT_STACK_CHECK:
				printf("EXCEPTION_FLT_STACK_CHECK\n");
				break;
			case EXCEPTION_FLT_UNDERFLOW:
				printf("EXCEPTION_FLT_UNDERFLOW\n");
				break;
			case EXCEPTION_INT_DIVIDE_BY_ZERO:
				printf("EXCEPTION_INT_DIVIDE_BY_ZERO\n");
				break;
			case EXCEPTION_INT_OVERFLOW:
				printf("EXCEPTION_INT_OVERFLOW\n");
				break;
			case EXCEPTION_PRIV_INSTRUCTION:
				printf("EXCEPTION_PRIV_INSTRUCTION\n");
				break;
			case EXCEPTION_IN_PAGE_ERROR:
				printf("EXCEPTION_IN_PAGE_ERROR\n");
				break;
			case EXCEPTION_ILLEGAL_INSTRUCTION:
				printf("EXCEPTION_ILLEGAL_INSTRUCTION\n");
				break;
			case EXCEPTION_NONCONTINUABLE_EXCEPTION:
				printf("EXCEPTION_NONCONTINUABLE_EXCEPTION\n");
				break;
			case EXCEPTION_STACK_OVERFLOW:
				printf("EXCEPTION_STACK_OVERFLOW\n");
				break;
			case EXCEPTION_INVALID_DISPOSITION:
				printf("EXCEPTION_INVALID_DISPOSITION\n");
				break;
			case EXCEPTION_GUARD_PAGE:
				printf("EXCEPTION_GUARD_PAGE\n");
				break;
			case EXCEPTION_INVALID_HANDLE:
				printf("EXCEPTION_INVALID_HANDLE\n");
				break;
			}
			break;
		}
		if (quit) {
			break;
		}
		if (!ContinueDebugEvent(de.dwProcessId, de.dwThreadId, dwStatus)) {
			break;
		}
	}
	DebugActiveProcessStop(pid);
	CloseHandle(h_process);
	for (;;) {
	}
	return (0);
}