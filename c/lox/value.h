#ifndef clox_value_h
#define clox_value_h

#include "common.h"

/* Some forward declarations due to circularity. */
typedef struct Obj Obj;
typedef struct ObjString ObjString;

typedef enum {
    VAL_BOOL,
    VAL_NIL,
    VAL_NUMBER,
    VAL_OBJ,
} ValueType;

/*
Currently the compiler will insert 4 bytes of padding. However,
moving "type" after "as" would not fix this, since an array of
"Values" would still be padded with 4 bytes between elements.
*/
typedef struct {
    ValueType type;  // 4 bytes. Immutable due to not pointer!
    union {
        bool boolean;
        double number;
        Obj* obj;
    } as;  // Tagged union. Currently 8 bytes.
} Value;

/* Check that a value is the correct type. */
#define IS_BOOL(value)      ((value).type == VAL_BOOL)
#define IS_NIL(value)       ((value).type == VAL_NIL)
#define IS_NUMBER(value)    ((value).type == VAL_NUMBER)
#define IS_OBJ(value)       ((value).type == VAL_OBJ)

/*
Converts a value to its "real" value in bytes.
Only to be used with the above 3 macros!!!
*/
#define AS_BOOL(value)      ((value).as.boolean)
#define AS_NUMBER(value)    ((value).as.number)
#define AS_OBJ(value)       ((value).as.obj)

/* Convert a "real" value to a clox Value struct. */
#define BOOL_VAL(value)     ((Value){VAL_BOOL, {.boolean = value}})
#define NIL_VAL             ((Value){VAL_NIL, {.number = 0}})
#define NUMBER_VAL(value)   ((Value){VAL_NUMBER, {.number = value}})
#define OBJ_VAL(value)      ((Value){VAL_OBJ, {.obj = value}})

typedef struct {
    int capacity;
    int count;
    Value* values;
} ValueArray;

bool valuesEqual(Value a, Value b);
void initValueArray(ValueArray* array);
void writeValueArray(ValueArray*, Value value);
void freeValueArray(ValueArray* array);
void printValue(Value value);

#endif