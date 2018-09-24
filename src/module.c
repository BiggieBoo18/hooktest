#include <stdio.h>
#include <windows.h>
#include <tlhelp32.h>
#include "module.h"
#include "util.h"

int module_list(int pid, PMODULEENTRY32 lpme) {
	int  i = 0;
	BOOL ret;
	MODULEENTRY32 me;
	HANDLE snapshot;

	me.dwSize = sizeof(me);
	snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid); // get snapshot
	if (snapshot == INVALID_HANDLE_VALUE) {
		return (-1);
	}
	if (Module32First(snapshot, &me)) { // get module
		do {
			lpme[i] = me;
			/* printf("MODULE_NAME: %s\n", me.szExePath); */
			i++;
		} while (Module32Next(snapshot, &me));
	}

	CloseHandle(snapshot); // close handle
	return (i);
}

FARPROC module_address(LPCSTR m_name, LPCSTR f_name) {
	HMODULE h_module;
	FARPROC address;

	h_module = GetModuleHandle(m_name);
	address = GetProcAddress(h_module, f_name);
	return (address);
}