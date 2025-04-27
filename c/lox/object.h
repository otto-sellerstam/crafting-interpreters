#ifndef clox_object_h
#define clox_object_h

#include "common.h"
#include "value.h"

#define OBJ_TYPE(value)     (AS_OBJ(value)->type)  // Why not just value->type?

#define IS_STRING(value)    isObjType(value, OBJ_STRING)

#define AS_STRING(value)    ((ObjString*)AS_OBJ(value))
#define AS_CSTRING(value)   (((ObjString*)AS_OBJ(value))->chars)

typedef enum {
    OBJ_STRING,
} ObjType;

struct Obj {
    ObjType type;
    struct Obj* next;
};

/*
C spec (6.7.2.1 13):

Within a structure object, the non-bit-field
members and the units in which bit-fields
reside have addresses that increase in the
order in which they are declared. A pointer
to a structure object, suitably converted,
points to its initial member (or if that
member is a bit-field, then to the unit in
which it resides), and vice versa. There
may be unnamed padding within a
structure object, but not at its beginning
*/
struct ObjString {
    Obj obj;  // Fields are expanded in place! Cool!
    int length;  // Effectively number of bytes.
    char* chars;  // Will be heap-allocated (ofc).
    uint32_t hash;  // For hash table (table.c).
};

ObjString* takeString(char* chars, int length);
ObjString* copyString(const char* chars, int length);
void printObject(Value value);

static inline bool isObjType(Value value, ObjType type) {
    return IS_OBJ(value) && OBJ_TYPE(value) == type;
}

#endif
