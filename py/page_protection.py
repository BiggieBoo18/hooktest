from ctypes    import *
from ctypes    import wintypes
from defines   import *
from privilege import set_debug_privilege

kernel32 = windll.kernel32

def get_page_info(h_process, address):
    mem_basic_info64 = MEMORY_BASIC_INFORMATION64()
    # print("address=0x{:016X}".format(address))
    if not kernel32.VirtualQueryEx(h_process,
                                   address,
                                   byref(mem_basic_info64),
                                   sizeof(mem_basic_info64)):
        print(WinError(GetLastError()))
        return False
    # print("Protect=0x{:016X}".format(mem_basic_info64.AllocationProtect))
    # print("RegionSize=", mem_basic_info64.RegionSize)
    # print("Protect=0x{:016X}".format(mem_basic_info64.Protect))
    return mem_basic_info64

def set_page_protection(h_process, address, size, new_protect):
    old_protect = wintypes.DWORD()
    if not kernel32.VirtualProtectEx(h_process,
                                     address,
                                     size,
                                     new_protect,
                                     byref(old_protect)):
        return False
    # print("old_protect=0x{:016X}".format(old_protect.value))
    return old_protect

def show_protection(protect):
    import defines
    vdir = vars(defines)
    res = [k for k, v in vdir.items() if v==protect and "PAGE" in k]
    if res:
        print("page_protect =", res[0])
    else:
        print("page_protect = UNKNOWN_PROTECT")

def test():
    def open_process(pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        # print("0x{:016X}".format(h_process))
        if not h_process:
            print(WinError(GetLastError()))
            return False
        return h_process

    set_debug_privilege()

    pid  = input("pid: ")

    snapshot    = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, int(pid))
    lpme        = MODULEENTRY32()
    lpme.dwSize = sizeof(lpme)
    res         = kernel32.Module32First(snapshot, byref(lpme))
    address     = None
    while res:
        if lpme.th32ProcessID==int(pid):
            if lpme.szModule==b"msctf.dll" or lpme.szModule==b"msvcrt.dll":
                print("PID:         ", lpme.th32ProcessID)
                print("MID:         ", lpme.th32ModuleID)
                # print("MODULE_ADDRESS 0x{:016X}".format(lpme.modBaseAddr))
                print("MODULE_SIZE: ", lpme.modBaseSize)
                print("MODULE_NAME: ", lpme.szModule)
                print("MODULE_PATH: ", lpme.szExePath)
                address = lpme.modBaseAddr
        res = kernel32.Module32Next(snapshot, byref(lpme))
    h_process = open_process(int(pid))
    if not h_process:
        print(WinError(GetLastError()))
        exit()
    p_address = cast(address, POINTER(BYTE))
    page_info = get_page_info(h_process, p_address)
    if not page_info:
        print(WinError(GetLastError()))
        exit()
    show_protection(page_info.Protect)
    old_protect = set_page_protection(h_process, p_address, page_info.RegionSize, PAGE_EXECUTE_READWRITE)
    if not old_protect:
        print(WinError(GetLastError()))
        exit()
    page_info = get_page_info(h_process, p_address)
    if not page_info:
        print(WinError(GetLastError()))
        exit()
    show_protection(page_info.Protect)

if __name__ == "__main__":
    test()
