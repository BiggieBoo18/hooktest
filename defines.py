from ctypes import *
from ctypes import wintypes
from enum   import Enum, auto

# types
BYTE      = wintypes.BYTE
WORD      = wintypes.WORD
DWORD     = wintypes.DWORD
DWORD64   = c_ulonglong
LONG      = wintypes.LONG
LPVOID    = wintypes.LPVOID
LPCVOID   = wintypes.LPCVOID
ULONG_PTR = wintypes.PULONG
ULONGLONG = c_ulonglong
LONGLONG  = c_longlong
TCHAR     = wintypes.CHAR
WCHAR     = wintypes.WCHAR
HMODULE   = wintypes.HMODULE

# constant
READ_CONTROL                      = 0x00020000
STANDARD_RIGHTS_REQUIRED          = 0x000F0000
STANDARD_RIGHTS_READ              = READ_CONTROL
STANDARD_RIGHTS_WRITE             = READ_CONTROL
STANDARD_RIGHTS_EXECUTE           = READ_CONTROL
SYNCHRONIZE                       = 0x00100000
DEBUG_PROCESS                     = 0x00000001
CREATE_NEW_CONSOLE                = 0x00000010
PROCESS_TERMINATE                 = 0x0001
PROCESS_CREATE_THREAD             = 0x0002
PROCESS_SET_SESSIONID             = 0x0004
PROCESS_VM_OPERATION              = 0x0008
PROCESS_VM_READ                   = 0x0010
PROCESS_VM_WRITE                  = 0x0020
PROCESS_DUP_HANDLE                = 0x0040
PROCESS_CREATE_PROCESS            = 0x0080
PROCESS_SET_QUOTA                 = 0x0100
PROCESS_SET_INFORMATION           = 0x0200
PROCESS_QUERY_INFORMATION         = 0x0400
PROCESS_SUSPEND_RESUME            = 0x0800
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_SET_LIMITED_INFORMATION   = 0x2000
PROCESS_ALL_ACCESS                = STANDARD_RIGHTS_REQUIRED|SYNCHRONIZE|0xFFFF
INFINITE                          = 0xFFFFFFFF
DBG_CONTINUE                      = 0x00010002
DBG_EXCEPTION_NOT_HANDLED         = 0x80010001
TH32CS_SNAPTHREAD                 = 0x00000004
TH32CS_SNAPMODULE                 = 0x00000008
THREAD_ALL_ACCESS                 = STANDARD_RIGHTS_REQUIRED|SYNCHRONIZE|0xFFFF
CONTEXT_AMD64                     = 0x00100000
CONTEXT_CONTROL                   = CONTEXT_AMD64|0x00000001
CONTEXT_INTEGER                   = CONTEXT_AMD64|0x00000002
CONTEXT_SEGMENTS                  = CONTEXT_AMD64|0x00000004
CONTEXT_FLOATING_POINT            = CONTEXT_AMD64|0x00000008
CONTEXT_DEBUG_REGISTERS           = CONTEXT_AMD64|0x00000010
CONTEXT_FULL                      = CONTEXT_CONTROL|CONTEXT_INTEGER|CONTEXT_FLOATING_POINT
CONTEXT_ALL                       = CONTEXT_CONTROL|CONTEXT_INTEGER|CONTEXT_SEGMENTS|CONTEXT_FLOATING_POINT|CONTEXT_DEBUG_REGISTERS
EXCEPTION_DEBUG_EVENT             = 1         
CREATE_THREAD_DEBUG_EVENT         = 2         
CREATE_PROCESS_DEBUG_EVENT        = 3         
EXIT_THREAD_DEBUG_EVENT           = 4         
EXIT_PROCESS_DEBUG_EVENT          = 5         
LOAD_DLL_DEBUG_EVENT              = 6         
UNLOAD_DLL_DEBUG_EVENT            = 7         
OUTPUT_DEBUG_STRING_EVENT         = 8         
RIP_EVENT                         = 9         
EXCEPTION_ACCESS_VIOLATION        = 0xC0000005
EXCEPTION_GUARD_PAGE_VIOLATION    = 0x80000001
EXCEPTION_BREAKPOINT              = 0x80000003
EXCEPTION_SINGLE_STEP             = 0x80000004
EXCEPTION_STACK_OVERFLOW          = 0xC00000FD
TOKEN_ASSIGN_PRIMARY              = 0x0001
TOKEN_DUPLICATE                   = 0x0002
TOKEN_IMPERSONATE                 = 0x0004
TOKEN_QUERY                       = 0x0008
TOKEN_QUERY_SOURCE                = 0x0010
TOKEN_ADJUST_PRIVILEGES           = 0x0020
TOKEN_ADJUST_GROUPS               = 0x0040
TOKEN_ADJUST_DEFAULT              = 0x0080
TOKEN_ADJUST_SESSIONID            = 0x0100
TOKEN_READ                        = STANDARD_RIGHTS_READ|TOKEN_QUERY
TOKEN_WRITE                       = STANDARD_RIGHTS_READ|TOKEN_ADJUST_PRIVILEGES|TOKEN_ADJUST_GROUPS|TOKEN_ADJUST_DEFAULT
TOKEN_ALL_ACCESS                  =  STANDARD_RIGHTS_REQUIRED|TOKEN_ASSIGN_PRIMARY|TOKEN_DUPLICATE|TOKEN_IMPERSONATE|TOKEN_QUERY|TOKEN_QUERY_SOURCE|TOKEN_ADJUST_PRIVILEGES|TOKEN_ADJUST_GROUPS|TOKEN_ADJUST_DEFAULT
SE_PRIVILEGE_ENABLED_BY_DEFAULT   = 0x00000001
SE_PRIVILEGE_ENABLED              = 0x00000002
SE_PRIVILEGE_REMOVED              = 0X00000004
SE_PRIVILEGE_USED_FOR_ACCESS      = 0x80000000
PAGE_NOACCESS                     = 0x01
PAGE_READONLY                     = 0x02
PAGE_READWRITE                    = 0x04
PAGE_WRITECOPY                    = 0x08
PAGE_EXECUTE                      = 0x10
PAGE_EXECUTE_READ                 = 0x20
PAGE_EXECUTE_READWRITE            = 0x40
PAGE_EXECUTE_WRITECOPY            = 0x80
PAGE_GUARD                        = 0x100
PAGE_NOCACHE                      = 0x200
PAGE_WRITECOMBINE                 = 0x400
PAGE_ENCLAVE_THREAD_CONTROL       = 0x80000000
PAGE_REVERT_TO_FILE_MAP           = 0x80000000
PAGE_TARGETS_NO_UPDATE            = 0x40000000
PAGE_TARGETS_INVALID              = 0x40000000
PAGE_ENCLAVE_UNVALIDATED          = 0x20000000
PAGE_ENCLAVE_DECOMMIT             = 0x10000000
MEM_COMMIT                        = 0x00001000
MEM_RESERVE                       = 0x00002000
MEM_REPLACE_PLACEHOLDER           = 0x00004000
MEM_RESERVE_PLACEHOLDER           = 0x00040000
MEM_RESET                         = 0x00080000
MEM_TOP_DOWN                      = 0x00100000
MEM_WRITE_WATCH                   = 0x00200000
MEM_PHYSICAL                      = 0x00400000
MEM_ROTATE                        = 0x00800000
MEM_DIFFERENT_IMAGE_BASE_OK       = 0x00800000
MEM_RESET_UNDO                    = 0x01000000
MEM_LARGE_PAGES                   = 0x20000000
MEM_4MB_PAGES                     = 0x80000000
MEM_64K_PAGES                     = MEM_LARGE_PAGES|MEM_PHYSICAL
MEM_UNMAP_WITH_TRANSIENT_BOOST    = 0x00000001
MEM_COALESCE_PLACEHOLDERS         = 0x00000001
MEM_PRESERVE_PLACEHOLDER          = 0x00000002
MEM_DECOMMIT                      = 0x00004000
MEM_RELEASE                       = 0x00008000
MEM_FREE                          = 0x00010000
CONDITION_EXECUTE                 = 0x0
CONDITION_WRITE_ONLY              = 0x1
CONDITION_IO_READ_WRITE           = 0x2
CONDITION_READ_WRITE              = 0x3
LENGTH_BYTE                       = 0x0
LENGTH_WORD                       = 0x1
LENGTH_QWORD                      = 0x2
LENGTH_DWORD                      = 0x3

class EXCEPTION_RECORD(Structure):
    pass

EXCEPTION_RECORD._fields_ = [
    ("ExceptionCode",        DWORD),
    ("ExceptionFlags",       DWORD),
    ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
    ("ExceptionAddress",     LPVOID),
    ("NumberParameters",     DWORD),
    ("ExceptionInformation", ULONG_PTR*15),
]

class EXCEPTION_RECORD(Structure):
    _fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     LPVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", ULONG_PTR*15),
    ]

class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord", EXCEPTION_RECORD),
        ("dwFirstCance",    DWORD),
    ]

class U(Union):
    _fields_ = [
        ("Exception", EXCEPTION_DEBUG_INFO),
    ]

class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode", DWORD),
        ("dwProcessId",      DWORD),
        ("dwThreadId",       DWORD),
        ("u",                U),
    ]

class THREADENTRY32(Structure):
    _fields_ = [
        ("dwSize",             DWORD),
        ("cntUsage",           DWORD),
        ("th32ThreadID",       DWORD),
        ("th32OwnerProcessID", DWORD),
        ("thBasePri",          LONG),
        ("thDeltaPri",         LONG),
        ("dwFlags",            DWORD),
    ]

class MODULEENTRY32(Structure):
    _fields_ = [
        ("dwSize",             DWORD),
        ("th32ModuleID",       DWORD),
        ("th32ProcessID",      DWORD),
        ("GlblcntUsage",       DWORD),
        ("ProccntUsage",       DWORD),
        ("modBaseAddr",        DWORD64),
        # ("modBaseAddr",        POINTER(BYTE)),
        ("modBaseSize",        DWORD),
        ("hModule",            HMODULE),
        ("szModule",           TCHAR*256),
        ("szExePath",          TCHAR*260),
    ]

class M128A(Structure):
    _fields_ = [
        ("Low",  ULONGLONG),
        ("High", LONGLONG),
    ]

class XSAVE_FORMAT(Structure):
    _fields_ = [
        ("ControlWord",    WORD), 
        ("StatusWord",     WORD), 
        ("TagWord",        BYTE), 
        ("Reservedl",      BYTE), 
        ("ErrorOpcode",    WORD), 
        ("ErrorOffset",    DWORD),
        ("ErrorSelector",  WORD), 
        ("Reserved2",      WORD), 
        ("DataOffset",     DWORD),
        ("DataSelector",   WORD), 
        ("Reserved3",      WORD), 
        ("MxCsr",          DWORD),
        ("MxCsr_Mask",     DWORD),
        ("FloatRegisters", M128A*8),
        ("XmmRegisters",   M128A*16),
        ("Reserved4",      BYTE*96),
    ]

class DUMMYSTRUCTNAME(Structure):
    _fields_ = [
        ("Header", M128A*2),
        ("Legacy", M128A*8),
        ("Xmm0",   M128A),
        ("Xmm1",   M128A),
        ("Xmm2",   M128A),
        ("Xmm3",   M128A),
        ("Xmm4",   M128A),
        ("Xmm5",   M128A),
        ("Xmm6",   M128A),
        ("Xmm7",   M128A),
        ("Xmm8",   M128A),
        ("Xmm9",   M128A),
        ("Xmm10",  M128A),
        ("Xmm11",  M128A),
        ("Xmm12",  M128A),
        ("Xmm13",  M128A),
        ("Xmm14",  M128A),
        ("Xmm15",  M128A),
    ]

XMM_SAVE_AREA32 = XSAVE_FORMAT
class DUMMYUNIONNAME(Union):
    _fields_ = [
        ("FltSave",         XMM_SAVE_AREA32),
        ("dummystructname", DUMMYSTRUCTNAME)
    ]

class CONTEXT(Structure):
    _pack_   = 16
    _fields_ = [
        ("P1Home",               DWORD64),
        ("P2Home",               DWORD64),
        ("P3Home",               DWORD64),
        ("P4Home",               DWORD64),
        ("P5Home",               DWORD64),
        ("P6Home",               DWORD64),
        ("ContextFlags",         DWORD),  
        ("MxCsr",                DWORD),  
        ("SegCs",                WORD),   
        ("SegDs",                WORD),   
        ("SegEs",                WORD),   
        ("SegFs",                WORD),   
        ("SegGs",                WORD),   
        ("SegSs",                WORD),   
        ("EFlags",               DWORD),  
        ("Dr0",                  DWORD64),
        ("Dr1",                  DWORD64),
        ("Dr2",                  DWORD64),
        ("Dr3",                  DWORD64),
        ("Dr6",                  DWORD64),
        ("Dr7",                  DWORD64),
        ("Rax",                  DWORD64),
        ("Rcx",                  DWORD64),
        ("Rdx",                  DWORD64),
        ("Rbx",                  DWORD64),
        ("Rsp",                  DWORD64),
        ("Rbp",                  DWORD64),
        ("Rsi",                  DWORD64),
        ("Rdi",                  DWORD64),
        ("R8",                   DWORD64),
        ("R9",                   DWORD64),
        ("R10",                  DWORD64),
        ("R11",                  DWORD64),
        ("R12",                  DWORD64),
        ("R13",                  DWORD64),
        ("R14",                  DWORD64),
        ("R15",                  DWORD64),
        ("Rip",                  DWORD64),
        ("dummyunionname",       DUMMYUNIONNAME),
        ("VectorRegister",       M128A*26),
        ("VectorControl",        DWORD64),
        ("DebugControl",         DWORD64),
        ("LastBranchToRip",      DWORD64),
        ("LastBranchFromRip",    DWORD64),
        ("LastExceptionToRip",   DWORD64),
        ("LastExceptionFromRip", DWORD64),
    ]

class LUID(Structure):
    _fields_ = [
        ("LowPart",  DWORD),
        ("HighPart", LONG),
    ]

class LUID_AND_ATTRIBUTES(Structure):
    _fields_ = [
        ("Luid",       LUID),
        ("Attributes", DWORD),
    ]

class TOKEN_PRIVILEGES(Structure):
    _fields_ = [
        ("PrivilegeCount", DWORD),
        ("Privileges",     LUID_AND_ATTRIBUTES*64),
    ]

class TOKEN_INFORMATION_CLASS(Enum):
    TokenUser                            = auto()
    TokenGroups                          = auto()
    TokenPrivileges                      = auto()
    TokenOwner                           = auto()
    TokenPrimaryGroup                    = auto()
    TokenDefaultDacl                     = auto()
    TokenSource                          = auto()
    TokenType                            = auto()
    TokenImpersonationLevel              = auto()
    TokenStatistics                      = auto()
    TokenRestrictedSids                  = auto()
    TokenSessionId                       = auto()
    TokenGroupsAndPrivileges             = auto()
    TokenSessionReference                = auto()
    TokenSandBoxInert                    = auto()
    TokenAuditPolicy                     = auto()
    TokenOrigin                          = auto()
    TokenElevationType                   = auto()
    TokenLinkedToken                     = auto()
    TokenElevation                       = auto()
    TokenHasRestrictions                 = auto()
    TokenAccessInformation               = auto()
    TokenVirtualizationAllowed           = auto()
    TokenVirtualizationEnabled           = auto()
    TokenIntegrityLevel                  = auto()
    TokenUIAccess                        = auto()
    TokenMandatoryPolicy                 = auto()
    TokenLogonSid                        = auto()
    TokenIsAppContainer                  = auto()
    TokenCapabilities                    = auto()
    TokenAppContainerSid                 = auto()
    TokenAppContainerNumber              = auto()
    TokenUserClaimAttributes             = auto()
    TokenDeviceClaimAttributes           = auto()
    TokenRestrictedUserClaimAttributes   = auto()
    TokenRestrictedDeviceClaimAttributes = auto()
    TokenDeviceGroups                    = auto()
    TokenRestrictedDeviceGroups          = auto()
    TokenSecurityAttributes              = auto()
    TokenIsRestricted                    = auto()
    MaxTokenInfoClass                    = auto()

class MEMORY_BASIC_INFORMATION64(Structure):
    _pack_   = 16
    _fields_ = [
        ("BaseAddress",       DWORD64),
        ("AllocationBase",    DWORD64),
        ("AllocationProtect", DWORD),
        ("__alignment1",      DWORD),
        ("RegionSize",        DWORD64),
        ("State",             DWORD),
        ("Protect",           DWORD),
        ("Type",              DWORD),
        ("__alignment2",      DWORD),
    ]

class PROCESSOR_ARCHITECTURE(Structure):
    _fields_ = [
        ("wProcessorArchitecture", WORD),
        ("wReserved",              WORD),
    ]

class U_PROCESSOR_ARCHITECTURE(Union):
    _fields_ = [
        ("dwOemId",                DWORD),
        ("proc_arch",              PROCESSOR_ARCHITECTURE),
    ]

class SYSTEM_INFO(Structure):
    _fields_ = [
        ("uproc_arch",                  U_PROCESSOR_ARCHITECTURE),
        ("dwPageSize",                  DWORD),
        ("lpMinimumApplivationAddress", LPVOID),
        ("lpMaximumApplivationAddress", LPVOID),
        ("dwActiveProcessorMask",       POINTER(DWORD)),
        ("dwNumberOfProcessors",        DWORD),
        ("dwProcessorType",             DWORD),
        ("wProcessorLevel",             WORD),
        ("wProcessorRevision",          WORD),
    ]
