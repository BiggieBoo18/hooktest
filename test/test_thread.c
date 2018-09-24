#include <stdio.h>
#include <windows.h>
#include <tlhelp32.h>
#include "thread.h"
#include "util.h"

int main(int argc, char *argv[]) {
  int            i=0, n=0, pid=-1;
  PTHREADENTRY32 lpte=NULL;
  CONTEXT        ct;
  HANDLE         h_thread;

  pid  = input_pid(); // input pid
  lpte = (PTHREADENTRY32)malloc(sizeof(lpte)*N_THREAD);
  n    = thread_list(pid, lpte);
  if (n==-1) {
    return (1);
  }
  printf("n=%d\n", n);
  for (i=0; i<n; i++) {
    printf("THREAD_ID: %d\n", lpte[i].th32ThreadID);
  }

  ct.ContextFlags = CONTEXT_FULL;
  h_thread = OpenThread(THREAD_ALL_ACCESS, FALSE, lpte[0].th32ThreadID);
  if (!h_thread) {
    show_error();
    free(lpte);
    return (1);
  }
  if (get_thread_context(h_thread, &ct)) {
    free(lpte);
    return (1);
  }
  puts("BEFORE");
  /* printf("[Rip]0x%016llX\n", ct.Rip); */
  printf("[Rbx]0x%016llX\n", ct.Rbx);
  /* printf("[Rsp]0x%016llX\n", ct.Rsp); */
  ct.Rbx = 0x1;
  if (set_thread_context(h_thread, &ct)) {
    free(lpte);
    return (1);
  }
  puts("AFTER");
  printf("[Rbx]0x%016llX\n", ct.Rbx);
  free(lpte);
  return (0);
}
