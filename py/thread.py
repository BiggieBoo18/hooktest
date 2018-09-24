from ctypes           import *
from ctypes           import wintypes
from defines          import *
from privilege        import set_debug_privilege, show_privilege_information

kernel32 = windll.kernel32

set_debug_privilege()

def open_thread(tid):
    h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, tid)
    if not h_thread:
        return True
    return h_thread

def get_thread_ids(pid):
    thread_ids = []
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, int(pid))
    lpte = THREADENTRY32()
    lpte.dwSize = sizeof(lpte)
    res = kernel32.Thread32First(snapshot, byref(lpte))
    while res:
        # print("PID: ", lpte.th32OwnerProcessID)
        if lpte.th32OwnerProcessID==pid:
            # print("    TID: 0x{:016X}".format(lpte.th32ThreadID))
            thread_ids.append(lpte.th32ThreadID)
        res = kernel32.Thread32Next(snapshot, byref(lpte))
    return thread_ids

def set_thread_context(h_thread, context):
    kernel32.SuspendThread(h_thread)
    if not kernel32.SetThreadContext(h_thread, byref(context)):
        return False
    kernel32.ResumeThread(h_thread)
    return True

def get_thread_context(h_thread):
    kernel32.SuspendThread(h_thread)
    context = CONTEXT()
    context.ContextFlags = CONTEXT_ALL
    res = kernel32.GetThreadContext(h_thread, byref(context))
    if not res:
        return False
    kernel32.ResumeThread(h_thread)
    return context

def main(pid):
    for tid in get_thread_ids(int(pid)):
        h_thread = open_thread(tid)
        if h_thread:
            context = get_thread_context(h_thread)
            context.Rdx = 0x7B # 123
            if not set_thread_context(h_thread, context):
                print(WinError(GetLastError()))
            if context:
                print("[Rip]0x{:016X}".format(context.Rip))
                print("[Rax]0x{:016X}".format(context.Rax))
                print("[Rcx]0x{:016X}".format(context.Rcx))
                print("[Rdx]0x{:016X}".format(context.Rdx))
                print("[Rbx]0x{:016X}".format(context.Rbx))
                print("[Rsp]0x{:016X}".format(context.Rsp))
                print("[Rbp]0x{:016X}".format(context.Rsp))
                print("[Rsi]0x{:016X}".format(context.Rsi))
                print("[Rdi]0x{:016X}".format(context.Rdi))
            else:
                print(WinError(GetLastError()))
    
if __name__ == "__main__":
    pid = int(input("pid: "))
    main(pid)
