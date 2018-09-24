#pragma once
#ifndef H_PRIVILEGE
#define H_PRIVILEGE

#define NAME_SIZE (256)

PTOKEN_PRIVILEGES get_privilege_information(void);
int set_debug_privilege(LPCSTR priv_name);
int show_privileges(void);

#endif