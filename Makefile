INCDIR  = /Iinclude
OBJ     = /Foobj/
BIN     = /OUT:bin/
OPT     = /Wall
CL      = cl
LINK    = link

# link
hook1: obj/hook1.obj obj/memory.obj obj/module.obj obj/privilege.obj obj/thread.obj obj/util.obj
	$(LINK) $(BIN)hook1.exe obj/hook1.obj obj/memory.obj obj/module.obj obj/privilege.obj obj/thread.obj obj/util.obj advapi32.lib
test_memory: obj/test_memory.obj obj/memory.obj obj/module.obj obj/util.obj
	$(LINK) $(BIN)test_memory.exe obj/test_memory.obj obj/memory.obj obj/module.obj obj/util.obj
# test_memory: obj/test_memory.obj obj/memory.obj obj/module.obj obj/thread.obj obj/util.obj
# 	$(LINK) $(BIN)test_memory.exe obj/test_memory.obj obj/memory.obj obj/module.obj obj/thread.obj obj/util.obj
test_module: obj/test_module.obj obj/module.obj obj/util.obj
	$(LINK) $(BIN)test_module.exe obj/test_module.obj obj/module.obj obj/util.obj
test_privilege: obj/test_privilege.obj obj/privilege.obj obj/util.obj
	$(LINK) $(BIN)test_privilege.exe obj/test_privilege.obj obj/privilege.obj obj/util.obj advapi32.lib
test_thread: obj/test_thread.obj obj/thread.obj obj/util.obj
	$(LINK) $(BIN)test_thread.exe obj/test_thread.obj obj/thread.obj obj/util.obj

# compile
obj/hook1.obj: src/hook1.c
	$(CL) $(INCDIR) $(OBJ) /c src/hook1.c
obj/test_module.obj: test/test_module.c
	$(CL) $(INCDIR) $(OBJ) /c test/test_module.c
obj/test_memory.obj: test/test_memory.c
	$(CL) $(INCDIR) $(OBJ) /c test/test_memory.c
obj/test_privilege.obj: test/test_privilege.c
	$(CL) $(INCDIR) $(OBJ) /c test/test_privilege.c
obj/test_thread.obj: test/test_thread.c
	$(CL) $(INCDIR) $(OBJ) /c test/test_thread.c
obj/memory.obj: src/memory.c
	$(CL) $(INCDIR) $(OBJ) /c src/memory.c
obj/module.obj: src/module.c
	$(CL) $(INCDIR) $(OBJ) /c src/module.c
obj/privilege.obj: src/privilege.c
	$(CL) $(INCDIR) $(OBJ) /c src/privilege.c
obj/thread.obj: src/thread.c
	$(CL) $(INCDIR) $(OBJ) /c src/thread.c
obj/util.obj: src/util.c
	$(CL) $(INCDIR) $(OBJ) /c src/util.c

clean:
	del obj/*.obj
