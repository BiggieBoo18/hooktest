from ctypes  import *
from ctypes  import wintypes
from defines import *

kernel32 = windll.kernel32
advapi32 = windll.advapi32

kernel32.GetCurrentProcess.argtypes = []
kernel32.GetCurrentProcess.restype  = wintypes.HANDLE

kernel32.OpenProcessToken.argtypes  = (
    wintypes.HANDLE,
    DWORD64,
    POINTER(wintypes.HANDLE)
)
kernel32.OpenProcessToken.restype   = wintypes.BOOL

advapi32.LookupPrivilegeNameW.argtypes = (
    wintypes.LPWSTR,
    POINTER(LUID),
    wintypes.LPWSTR,
    POINTER(wintypes.DWORD)
)
advapi32.LookupPrivilegeNameW.restype  = wintypes.BOOL

advapi32.LookupPrivilegeDisplayNameW.argtypes = (
    wintypes.LPWSTR,
    wintypes.LPWSTR,
    wintypes.LPWSTR,
    POINTER(wintypes.DWORD),
    POINTER(wintypes.DWORD)
)
advapi32.LookupPrivilegeDisplayNameW.restype  = wintypes.BOOL

def get_token():
    token  = wintypes.HANDLE()
    handle = kernel32.GetCurrentProcess()
    if not kernel32.OpenProcessToken(handle, TOKEN_ALL_ACCESS, token):
        return False
    return token

def get_luid():
    luid = LUID()
    if not advapi32.LookupPrivilegeValueW(None, "seDebugPrivilege", byref(luid)):
        return False
    return luid

def get_privilege_information():
    token                   = get_token()
    token_information_class = TOKEN_INFORMATION_CLASS.TokenPrivileges.value
    return_length           = wintypes.DWORD()
    res = advapi32.GetTokenInformation(token,
                                       token_information_class,
                                       None,
                                       0,
                                       byref(return_length))
    buffer = create_string_buffer(return_length.value)
    res = advapi32.GetTokenInformation(token,
                                       token_information_class,
                                       buffer,
                                       return_length.value,
                                       byref(return_length))
    if not res:
        return False
    privileges = cast(buffer, POINTER(TOKEN_PRIVILEGES)).contents
    return privileges

def enable_privilege(token, luid):
    l_and_a            = LUID_AND_ATTRIBUTES()
    l_and_a.Luid       = luid
    l_and_a.Attributes = SE_PRIVILEGE_ENABLED
    tp                 = TOKEN_PRIVILEGES()
    tp.PrivilegeCount  = 1
    tp.Privileges[0]   = l_and_a
    if not advapi32.AdjustTokenPrivileges(token, False, byref(tp), 0, 0, 0):
        return False
    return True

def set_debug_privilege():
    token = get_token()
    if not token:
        print(WinError(GetLastError()))
        exit()
    luid = get_luid()
    if not luid:
        print(WinError(GetLastError()))
        exit()
    enable_privilege(token, luid)
    if GetLastError()!=0:
        # print("[!!] enable_privilege Error")
        return False
    else:
        # print("[*] enabled debug privilege")
        return True

def show_privilege_information():
    privileges = get_privilege_information()
    for i in range(privileges.PrivilegeCount):
        return_length  = wintypes.DWORD(10240)
        language_id    = wintypes.DWORD(128)
        display_name   = create_unicode_buffer(return_length.value)
        privilege_name = create_unicode_buffer(return_length.value)
        enabled = bool(privileges.Privileges[i].Attributes & SE_PRIVILEGE_ENABLED)
        res = advapi32.LookupPrivilegeNameW(None,
                                            privileges.Privileges[i].Luid,
                                            privilege_name,
                                            return_length)
        if not res:
            continue
        privilege_name = str(privilege_name[:return_length.value])
        res = advapi32.LookupPrivilegeDisplayNameW(None,
                                                   privilege_name,
                                                   display_name,
                                                   return_length,
                                                   language_id)
        if not res:
            continue
        display_name = str(display_name[:return_length.value])
        print("{}({}) : {}".format(privilege_name, display_name, enabled))

if __name__ == "__main__":
    show_privilege_information()
    set_debug_privilege()
    show_privilege_information()
