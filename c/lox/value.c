#include <stdio.h>
#include <string.h>

#include "memory.h"
#include "object.h"
#include "value.h"

void initValueArray(ValueArray* array) {
    array->count = 0;
    array->capacity = 0;
    array->values = NULL;
}

void writeValueArray(ValueArray* array, Value value) {
    if (array->capacity < array->count + 1) {
        int oldCapacity = array->capacity;
        array->capacity = GROW_CAPACITY(oldCapacity);
        array->values = GROW_ARRAY(
            Value,
            array->values,
            oldCapacity,
            array->capacity
        );
    }

    array->values[array->count++] = value;
}

void freeValueArray(ValueArray* array) {
    FREE_ARRAY(Value, array->values, array->capacity);
    initValueArray(array);
}

void printValue(Value value) {
    switch (value.type) {
        case VAL_BOOL: {
            printf(AS_BOOL(value) ? "true" : "false");
            break;
        }
        case VAL_NIL: {
            printf("nil");
            break;
        }
        case VAL_NUMBER: {
            printf("%g", AS_NUMBER(value));
            break;
        }
        case VAL_OBJ: {
            printObject(value);
            break;
        }
    }
}

/*
mcmcmp can't be used due to padding. Two "equal" Values might
be "unequal" in memory due to unused bytes.
*/
bool valuesEqual(Value a, Value b) {
    if (a.type != b.type) return false;
    switch (a.type) {
        case VAL_BOOL:
            return AS_BOOL(a) == AS_BOOL(b);
        case VAL_NIL:
            return true;
        case VAL_NUMBER:
            return AS_NUMBER(a) == AS_NUMBER(b);
        case VAL_OBJ:
            return AS_OBJ(a) == AS_OBJ(b);  // Works because if string interning!
        default:
            return false;
    }
}