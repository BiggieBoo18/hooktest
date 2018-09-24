import random

from ctypes       import *

from defines      import *
from func_resolve import func_resolve
from memory       import write_process_memory, read_process_memory, set_sw_bp, sw_bp_postproc
from thread       import open_thread, get_thread_context, set_thread_context

kernel32 = windll.kernel32

def show_error(h_process=None, pid=None):
    print(WinError(GetLastError()))
    if pid:
        kernel32.DebugActiveProcessStop(pid)
    if h_process:
        kernel32.CloseHandle(h_process)
    exit(1)

def hook_proc(h_process, tid):
    h_thread = open_thread(tid)
    if not h_thread:
        return False
    context = get_thread_context(h_thread)
    if not context:
        return False
    # print("[Rip]0x{:016X}".format(context.Rip))
    # print("[Rax]0x{:016X}".format(context.Rax))
    # print("[Rcx]0x{:016X}".format(context.Rcx))
    # print("[Rdx]0x{:016X}".format(context.Rdx))
    # print("[Rbx]0x{:016X}".format(context.Rbx))
    # print("[Rsp]0x{:016X}".format(context.Rsp))
    # print("[Rbp]0x{:016X}".format(context.Rbp))
    # print("[Rsi]0x{:016X}".format(context.Rsi))
    # print("[Rdi]0x{:016X}".format(context.Rdi))
    print("[R8]0x{:016X}".format(context.R8))
    context.R8 = random.randint(0, 1000)
    set_thread_context(h_thread, context)
    return True

pid = int(input("pid: "))
# open process
h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
if not h_process:
    show_error()
# attach process
if not kernel32.DebugActiveProcess(pid):
    show_error(h_process=h_process)

sw_bps      = {}
address     = func_resolve("kernel32.dll", b"WriteFile")
debug_event = DEBUG_EVENT()
first_break = False # windows break
counter     = 0
while True:
    # set breakpoint
    if not set_sw_bp(h_process, address, sw_bps):
        show_error(h_process=h_process, pid=pid)
    if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
        # print(debug_event.dwDebugEventCode)
        exception_record = debug_event.u.Exception.ExceptionRecord
        if debug_event.dwDebugEventCode==1 and exception_record.ExceptionCode==EXCEPTION_BREAKPOINT: # exception breakpoint
            if first_break:
                hook_proc(h_process, debug_event.dwThreadId)
                sw_bp_address = sw_bp_postproc(h_process, debug_event.dwThreadId, sw_bps, exception_record.ExceptionAddress)
                if not sw_bp_address:
                    show_error(h_process=h_process, pid=pid)
                print("counter = {}".format(counter))
                counter += 1
            else:
                first_break = True
        kernel32.ContinueDebugEvent(debug_event.dwProcessId,
                                    debug_event.dwThreadId,
                                    DBG_CONTINUE)
        if counter>=5:
            break
kernel32.DebugActiveProcessStop(pid)
kernel32.CloseHandle(h_process)
