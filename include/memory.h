#pragma once
#ifndef H_MEMORY
#define H_MEMORY

#define BUF_SIZE (1)

int get_page_info(HANDLE h_process, LPVOID address, PMEMORY_BASIC_INFORMATION lpmbi);
DWORD set_page_protection(HANDLE h_process, LPVOID address, DWORD size, DWORD new_protect);
SIZE_T read_process_memory(HANDLE h_process, LPVOID address, LPVOID buf, SIZE_T size);
SIZE_T write_process_memory(HANDLE h_process, LPVOID address, LPCVOID buf, SIZE_T size);
int set_sw_bp(HANDLE h_process, LPVOID address, LPVOID orig_byte);
int sw_bp_post_proc(HANDLE h_process, HANDLE h_thread, LPVOID address, LPVOID orig_byte);

#endif