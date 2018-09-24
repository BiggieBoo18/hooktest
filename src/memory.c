#include <stdio.h>
#include <windows.h>
#include "memory.h"
#include "thread.h"
#include "util.h"

int get_page_info(HANDLE h_process, LPVOID address, PMEMORY_BASIC_INFORMATION lpmbi) {
	if (!VirtualQueryEx(h_process, address, *(&lpmbi), sizeof(*lpmbi))) {
		show_error();
		return (1);
	}
	/* printf("protect=0x%lX\n", lpmbi->Protect); */
	return (0);
}

DWORD set_page_protection(HANDLE h_process, LPVOID address, DWORD size, DWORD new_protect) {
	DWORD old_protect = 0;

	if (!VirtualProtectEx(h_process, address, size, new_protect, &old_protect)) {
		show_error();
	}
	return (old_protect);
}

SIZE_T read_process_memory(HANDLE h_process, LPVOID address, LPVOID buf, SIZE_T size) {
	MEMORY_BASIC_INFORMATION mbi;
	DWORD                    old_protect = 0;
	SIZE_T                   count = 0;

	if (get_page_info(h_process, address, &mbi)) {
		return (0);
	}
	old_protect = set_page_protection(h_process, address, (DWORD)size, PAGE_EXECUTE_READWRITE);
	if (!old_protect) {
		return (0);
	}
	if (!ReadProcessMemory(h_process, address, *(&buf), size, &count)) {
		show_error();
		return (0);
	}

	if (!set_page_protection(h_process, address, (DWORD)size, old_protect)) {
		return (0);
	}
	return (count);
}

SIZE_T write_process_memory(HANDLE h_process, LPVOID address, LPCVOID buf, SIZE_T size) {
	MEMORY_BASIC_INFORMATION mbi;
	DWORD                    old_protect = 0;
	SIZE_T                   count = 0;

	if (get_page_info(h_process, address, &mbi)) {
		return (0);
	}
	old_protect = set_page_protection(h_process, address, (DWORD)size, PAGE_EXECUTE_READWRITE);
	if (!old_protect) {
		return (0);
	}
	if (!WriteProcessMemory(h_process, address, buf, size, &count)) {
		show_error();
		return (0);
	}
	if (!FlushInstructionCache(h_process, NULL, 0)) {
		show_error();
		return (0);
	}
	if (!set_page_protection(h_process, address, (DWORD)size, old_protect)) {
		return (0);
	}
	return (count);
}

int set_sw_bp(HANDLE h_process, LPVOID address, LPVOID orig_byte) {
	SIZE_T count = 0;
	char   int3[BUF_SIZE] = { 0xCC };

	count = read_process_memory(h_process, address, *(&orig_byte), BUF_SIZE);
	if (!count) {
		return (1);
	}
	printf("orig_byte=%x\n", ((char *)orig_byte)[0] & 0xff);

	count = write_process_memory(h_process, address, &int3, BUF_SIZE);
	if (!count) {
		return (1);
	}
	return (0);
}

int sw_bp_post_proc(HANDLE h_process, HANDLE h_thread, LPVOID address, LPVOID orig_byte) {
	CONTEXT ct;
	SIZE_T  count = 0;
	char    bf[BUF_SIZE];

	printf("orig_byte=%x\n", ((char *)orig_byte)[0] & 0xff);

	SuspendThread(h_thread);
	ct.ContextFlags = CONTEXT_FULL;
	if (get_thread_context(h_thread, &ct)) {
		return (1);
	}
	count = write_process_memory(h_process, address, orig_byte, BUF_SIZE);
	if (!count) {
		return (1);
	}
	ct.Rip--;
	if (set_thread_context(h_thread, &ct)) {
		return (1);
	}

	// debug
	ct.ContextFlags = CONTEXT_FULL;
	if (get_thread_context(h_thread, &ct)) {
		return (1);
	}
	printf("rip=%016llX\n", ct.Rip);

	count = read_process_memory(h_process, address, &bf, BUF_SIZE);
	if (!count) {
		return (1);
	}
	printf("return_code=%x\n", bf[0] & 0xff);

	ResumeThread(h_thread);
	return (0);
}
