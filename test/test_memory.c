#include <stdio.h>
#include <windows.h>
#include <tlhelp32.h>
#include "memory.h"
#include "module.h"
#include "thread.h"
#include "util.h"

int main(int argc, char *argv[]) {
  int                      i=0, n=0, pid=-1;
  HANDLE                   h_process;
  FARPROC                  address;
  MEMORY_BASIC_INFORMATION mbi;
  DWORD                    old_protect;
  char                     read_buf[BUF_SIZE];
  char                     orig_byte[BUF_SIZE];
  char                     write_buf[] = {0xcc};
  SIZE_T                   count=0;

  pid = input_pid();
  h_process = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
  if (!h_process) {
    show_error();
    return (1);
  }
  address = module_address("KERNEL32.DLL", "WriteFile");
  if (!address) {
    return (1);
  }
  printf("address=0x%016p\n", address);
  if (get_page_info(h_process, address, &mbi)) {
    return (1);
  }
  printf("protect=0x%lX\n", mbi.Protect);
  old_protect = set_page_protection(h_process, address, mbi.RegionSize, PAGE_EXECUTE_READWRITE);
  if (!old_protect) {
    return (1);
  }
  printf("old_protect=0x%lX\n", old_protect);
  if (get_page_info(h_process, address, &mbi)) {
    return (1);
  }
  printf("new_protect=0x%lX\n", mbi.Protect);
  if (!set_page_protection(h_process, address, mbi.RegionSize, old_protect)) {
    return (1);
  }
  printf("size=%zd\n", sizeof(read_buf));
  count = read_process_memory(h_process, address, &read_buf, sizeof(read_buf));
  if (!count) {
    return (1);
  }
  printf("read_buf=%x %zd\n", read_buf[0]&0xff, count);
  set_sw_bp(h_process, address, &orig_byte);
  printf("orig_byte=%x %zd\n", orig_byte[0]&0xff, count);
  /* count = write_process_memory(h_process, address, &write_buf, sizeof(write_buf)); */
  /* if (!count) { */
  /*   return (1); */
  /* } */
  /* printf("write=%zd\n", count);   */
  count = read_process_memory(h_process, address, &read_buf, sizeof(read_buf));
  if (!count) {
    return (1);
  }
  printf("read_buf=%x %zd\n", read_buf[0]&0xff, count);

  return (0);
}
