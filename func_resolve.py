from ctypes  import *
from ctypes  import wintypes
from defines import *

kernel32 = windll.kernel32

kernel32.GetModuleHandleW.argtypes = [
    wintypes.LPCWSTR,
]
kernel32.GetModuleHandleW.restype  = wintypes.HMODULE

kernel32.GetProcAddress.argtypes = [
    wintypes.HMODULE,
    wintypes.LPCVOID,
]
kernel32.GetProcAddress.restype = DWORD64

def func_resolve(dll, function):
    h_module = kernel32.GetModuleHandleW(dll)
    if not h_module:
        return False
    # print("h_module=0x{:016X}".format(h_module))
    address  = kernel32.GetProcAddress(h_module, function)
    if not address:
        return False
    # print("address=0x{:016X}".format(address))
    return address

if __name__ == "__main__":
    address = func_resolve("ucrtbased.dll", b"__stdio_common_vfprintf")
    print("address=0x{:016X}".format(address))
