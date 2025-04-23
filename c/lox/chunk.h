#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"
#include "value.h"

// Bytecode instructions (OpCode = Operation Code)
typedef enum {
    OP_CONSTANT,
    OP_RETURN,
} OpCode;

// Dynamic array of instructions.
typedef struct {
    int capacity; // Number of allocated elements.
    int count; // Number of allocated elements in use.
    uint8_t* code; // Byte codes (uint8_t = 8 bits = 1 byte).
    int* lines; // Line numbers of bytecodes. Hilariously inefficient in terms of memory!
    ValueArray constants; // Constant values. Corresponding indices stored in "code".
} Chunk;

void initChunk(Chunk* cunk);
void writeChunk(Chunk* chunk, uint8_t byte, int line);
int addConstant(Chunk*, Value value);
void freeChunk(Chunk* chunk);

#endif