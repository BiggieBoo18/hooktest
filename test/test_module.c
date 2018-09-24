#include <stdio.h>
#include <windows.h>
#include <tlhelp32.h>
#include "module.h"
#include "util.h"

int main(int argc, char *argv[]) {
  int i=0, n=0, pid=-1;
  PMODULEENTRY32 lpme = NULL;

  pid = input_pid(); // input pid
  lpme = (PMODULEENTRY32)malloc(sizeof(lpme)*N_MODULE);
  n = module_list(pid, lpme);
  if (n==-1) {
    return 1;
  }
  printf("%d\n", n);
  for (i=0; i<n; i++) {
    printf("MODULE_NAME: %s\n", lpme[i].szExePath);
  }
  
  FARPROC address;
  address = module_address("KERNEL32.DLL", "WriteFile");
  if (address) {
    printf("true\n");
    printf("%p\n", address);
  } else {
    printf("false\n");
  }

  free(lpme);
}
