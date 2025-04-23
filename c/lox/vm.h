#ifndef clox_vm_h
#define clox_vm_h

#include "chunk.h"
#include "value.h"

#define STACK_MAX 256

typedef struct {
    Chunk* chunk;
    uint8_t* ip; /* Instruction Pointer: Keeps track of the current bytecode
    to execute. Optimal would be to keep ip local to have the C compiler keep
    it in a CPU register. Sometimes "PC" for Program Counter. */
    Value stack[STACK_MAX]; /* The stack itself. */
    Value* stackTop; /* Stack pointer! Points at the element just past the top value. */
} VM;

typedef enum {
    INTERPRET_OK,
    INTERPRET_COMPILE_ERROR,
    INTERPRET_RUNTIME_ERROR
} InterpretResult;

void initVM();
void freeVM();
InterpretResult interpret(Chunk* chunk);
void push(Value value);
Value pop();

#endif