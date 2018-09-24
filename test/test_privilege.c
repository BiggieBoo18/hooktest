#include <stdio.h>
#include <windows.h>
#include "privilege.h"
#include "util.h"

int main(int argc, char *argv[]) {
  int ret = 0;
  
  printf("BEFORE\n");
  show_privileges();
  ret = set_debug_privilege("seDebugPrivilege");
  if (ret) {
    printf("ret=%d\n", ret);
    show_error();
    return (1);
  }
  printf("AFTER\n");
  show_privileges();

  return (0);
}
