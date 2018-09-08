from ctypes          import *
from defines         import *
from privilege       import set_debug_privilege
from page_protection import get_page_info, set_page_protection, show_protection
from thread          import open_thread, get_thread_context, set_thread_context

kernel32 = windll.kernel32

set_debug_privilege()

def read_process_memory(h_process, address, length):
    page_info = get_page_info(h_process, address)
    if not page_info:
        return False
    old_protect = set_page_protection(h_process, address, page_info.RegionSize, PAGE_EXECUTE_READWRITE)
    data     = ""
    read_buf = create_string_buffer(length)
    count    = c_ulonglong(0)
    if not kernel32.ReadProcessMemory(h_process, address, read_buf, length, byref(count)):
        return False
    else:
        data = read_buf.raw.hex()
        return data

def write_process_memory(h_process, address, data):
    page_info = get_page_info(h_process, address)
    if not page_info:
        return False
    old_protect = set_page_protection(h_process, address, page_info.RegionSize, PAGE_EXECUTE_READWRITE)
    if not kernel32.WriteProcessMemory(h_process, address, data, len(data), 0):
        return False
    kernel32.FlushInstructionCache(h_process, None, 0)
    return True

def set_sw_bp(h_process, address, sw_bps):
    p_address = cast(address, POINTER(BYTE))
    if address not in [v[0] for v in sw_bps.values()]:
        original_byte = read_process_memory(h_process, p_address, 1)
        if not original_byte:
            return False
        if not write_process_memory(h_process, p_address, "\xCC"):
            return False
        sw_bps[len(sw_bps)] = (address, original_byte)
        return sw_bps
    return sw_bps

def sw_bp_postproc(h_process, tid, sw_bps, exception_address):
    break_info = [info for info in sw_bps.values() if info[0]==exception_address] # address and original_byte at break point
    break_idx = [k for k, info in sw_bps.items() if info[0]==exception_address]
    if not break_info:
        return False
    break_info = break_info[0]
    h_thread = open_thread(tid)
    if not h_thread:
        return False
    context = get_thread_context(h_thread)
    if not context:
        return False
    if not write_process_memory(h_process, cast(break_info[0], POINTER(BYTE)), bytes.fromhex(break_info[1])):
        return False
    context.Rip    -= 0x1
    # context.EFlags |= 1<<8
    if not set_thread_context(h_thread, context):
        return False
    context = get_thread_context(h_thread)
    if not context:
        return False
    for k in break_idx:
        sw_bps.pop(k)
    return break_info[0]
