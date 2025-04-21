#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"

// Bytecode instructions (OpCode = Operation Code)
typedef enum {
    OP_RETURN,
} OpCode;

// Dynamic array of instructions.
typedef struct {
    int capacity; // Number of allocated elements.
    int count; // Number of allocated elements in use.
    uint8_t* code;
} Chunk;

void initChunk(Chunk* cunk);
void writeChunk(Chunk* chunk, uint8_t byte);
void freeChunk(Chunk* chunk);

#endif