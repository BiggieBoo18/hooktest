import time
import os

from ctypes  import *

msvcrt = cdll.msvcrt

i   = 0
pid = os.getpid()
while True:
    msvcrt.wprintf("[%d]Loop iteration %d!\n", pid, i)
    i += 1
    time.sleep(1)
