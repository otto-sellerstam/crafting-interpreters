#ifndef clox_chunk_h
#define clox_chunk_h

#include "common.h"
#include "value.h"

// Bytecode instructions (OpCode = Operation Code)
// I don't implement >=, <= and != for the sake of learning! Although
// this doesn't follow IEEE 754.
typedef enum {
    OP_CONSTANT,
    OP_NIL,
    OP_TRUE,
    OP_FALSE,
    OP_POP,
    OP_GET_LOCAL,
    OP_GET_GLOBAL,
    OP_DEFINE_GLOBAL,
    OP_SET_LOCAL,
    OP_SET_GLOBAL,
    OP_EQUAL,  
    OP_GREATER,
    OP_LESS,
    OP_ADD,
    OP_SUBTRACT,
    OP_MULTIPLY,
    OP_DIVIDE,
    OP_NOT,
    OP_NEGATE,
    OP_PRINT,
    OP_JUMP,
    OP_JUMP_IF_FALSE,
    OP_LOOP,
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