#ifndef clox_vm_h
#define clox_vm_h

#include "chunk.h"
#include "table.h"
#include "value.h"

#define STACK_MAX 256

typedef struct {
    Chunk* chunk;  // Chunk of bytecodes.
    uint8_t* ip; /* Instruction Pointer: Keeps track of the current bytecode
    to execute. Optimal would be to keep ip local to have the C compiler keep
    it in a CPU register. Sometimes "PC" for Program Counter. */
    Value stack[STACK_MAX]; /* The stack itself. */
    Value* stackTop; /* Stack pointer! Points at the element just past the top value. */
    Table globals;  // Hash table for global variables.
    Obj* objects;  // Intrusive list.
    Table strings;  // clox interns all strings.
} VM;

typedef enum {
    INTERPRET_OK,
    INTERPRET_COMPILE_ERROR,
    INTERPRET_RUNTIME_ERROR
} InterpretResult;

extern VM vm;

void initVM();
void freeVM();
InterpretResult interpret(const char* source);
void push(Value value);
Value pop();

#endif