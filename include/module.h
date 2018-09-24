#pragma once
#ifndef H_MODULE
#define H_MODULE

#define N_MODULE (256)

int     module_list(int pid, PMODULEENTRY32 lpme);
FARPROC module_address(LPCSTR m_name, LPCSTR f_name);

#endif