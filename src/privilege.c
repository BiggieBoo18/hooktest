#include <stdio.h>
#include <windows.h>
#include "util.h"

#define NAME_SIZE (256)

PTOKEN_PRIVILEGES get_privilege_information(void) {
	HANDLE            token;
	DWORD             dwReturnLength;
	PTOKEN_PRIVILEGES p_tp;

	if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ALL_ACCESS, &token)) { // get token
		return (NULL);
	}
	GetTokenInformation(token, TokenPrivileges, NULL, 0, &dwReturnLength);
	p_tp = (PTOKEN_PRIVILEGES)malloc(LPTR*dwReturnLength);
	if (!p_tp) {
		CloseHandle(token);
		return (NULL);
	}
	GetTokenInformation(token, TokenPrivileges, p_tp, dwReturnLength, &dwReturnLength);
	return (p_tp);
}

int set_debug_privilege(LPCSTR priv_name) {
	HANDLE           token;
	LUID             luid;
	TOKEN_PRIVILEGES tp;

	if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ALL_ACCESS, &token)) { // get token
		return (1);
	}
	if (!LookupPrivilegeValue(NULL, priv_name, &luid)) { // get luid
		return (1);
	}
	tp.PrivilegeCount = 1;
	tp.Privileges[0].Luid = luid;
	tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
	if (!AdjustTokenPrivileges(token, FALSE, &tp, 0, 0, 0)) {
		return (1);
	}
	CloseHandle(token);
	return (0);
}

int show_privileges(void) {
	int               i = 0, length = 0, lang_id = 0;
	char              PrivilegeName[NAME_SIZE];
	char              DisplayName[NAME_SIZE];
	PTOKEN_PRIVILEGES p_tp = NULL;

	p_tp = get_privilege_information();
	/* printf("privileges=%p, c=%d\n", p_tp, p_tp->PrivilegeCount); */
	for (i = 0; i < p_tp->PrivilegeCount; i++) {
		length = sizeof(PrivilegeName) / sizeof(PrivilegeName[0]);
		LookupPrivilegeName(NULL,
			&p_tp->Privileges[i].Luid,
			PrivilegeName,
			&length);
		length = sizeof(DisplayName) / sizeof(PrivilegeName[0]);
		LookupPrivilegeDisplayName(NULL,
			PrivilegeName,
			DisplayName,
			&length,
			&lang_id);
		puts("------------------------------------");
		printf("PrivilegeName: %s\n", PrivilegeName);
		printf("DisplayName:   %s\n", DisplayName);
		printf("%s\n", p_tp->Privileges[i].Attributes&SE_PRIVILEGE_ENABLED ? "True" : "False");
	}
	puts("------------------------------------");
	free(p_tp);
	return (0);
}