#pragma once
#ifndef H_THREAD
#define H_THREAD

#include <tlhelp32.h>

#define N_THREAD (256)

int thread_list(int pid, PTHREADENTRY32 lpte);
int set_thread_context(HANDLE h_thread, CONTEXT *ct);
int get_thread_context(HANDLE h_thread, CONTEXT *ct);
int switch_TF(HANDLE h_thread);

#endif