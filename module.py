from ctypes    import *
from ctypes    import wintypes
from defines   import *
from privilege import set_debug_privilege

kernel32 = windll.kernel32

set_debug_privilege()

def to_dict(lpme):
    return dict((field, getattr(lpme, field)) for field, _ in lpme._fields_)

def enum_modules(pid):
    module_list = []
    snapshot    = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE,
                                                    int(pid))
    lpme        = MODULEENTRY32()
    lpme.dwSize = sizeof(lpme)
    res         = kernel32.Module32First(snapshot, byref(lpme))
    while res:
        if lpme.th32ProcessID==int(pid):
            module_list.append(to_dict(lpme))
            # print("PID:         ", lpme.th32ProcessID)
            # print("MID:         ", lpme.th32ModuleID)
            print("MODULE_NAME: ", lpme.szModule)
            # print("MODULE_PATH: ", lpme.szExePath)
        res = kernel32.Module32Next(snapshot, byref(lpme))
    return module_list

if __name__ == "__main__":
    pid = int(input("pid: "))
    enum_modules(pid)
