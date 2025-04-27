#include <stdlib.h>
#include <string.h>

#include "memory.h"
#include "object.h"
#include "table.h"
#include "value.h"

#define TABLE_MAX_LOAD 0.75

void initTable(Table* table) {
    table->count = 0;
    table->capacity = 0;
    table->entries = NULL;
}

void freeTable(Table* table) {
    FREE_ARRAY(Entry, table->entries, table->capacity);
    initTable(table);
}

static Entry* findEntry(
    Entry* entries,
    int capacity,
    ObjString* key
) {
    // Start where we'd "expect" to find it.
    uint32_t index = key->hash % capacity;
    Entry* tombstone = NULL;

    for (;;) {
        // Get entry at index.
        Entry* entry = entries + index;
        if (entry->key == NULL) {
            if (IS_NIL(entry->value)) {
                // Emptry entry.
                return tombstone != NULL ? tombstone : entry;
            } else {
                // We found a tombstone.
                if (tombstone == NULL) tombstone = entry;
            }
        } else  if (entry->key == key) {
            // Return found key.
            return entry;
        }

        // Probe and walk forward! We only reach this if there's been a collision.
        index = (index + 1) % capacity;
    }
}

bool tableGet(Table* table, ObjString* key, Value* value) {
    if (table->count == 0) return false;

    Entry* entry = findEntry(table->entries, table->capacity, key);
    if (entry->key == NULL) return false;

    *value = entry->value;
    return true;
}

static void adjustCapacity(Table* table, int capacity) {
    // First create new entries.
    Entry* entries = ALLOCATE(Entry, capacity);
    
    for (int i = 0; i < capacity; i++) {
        entries[i].key = NULL;
        entries[i].value = NIL_VAL;
    }

    // Then "copy over" values from table into the new entries.
    table->count = 0;
    for (int i = 0; i < table->capacity; i++) {
        Entry* entry = &table->entries[i];
        if (entry->key == NULL) continue;

        // Find a pointer to the entry in entries, and modify it's value in place.
        Entry* dest = findEntry(entries, capacity, entry->key);
        dest->key = entry->key;
        dest->value = entry->value;
        table->count++;
    }

    FREE_ARRAY(Entry, table->entries, table->capacity);
    table->entries = entries;
    table->capacity = capacity;
}

bool tableSet(Table* table, ObjString* key, Value value) {
    // Add element to hash table.

    // If the tash table count is too large, grow the table.
    if (table->count + 1 > table->capacity * TABLE_MAX_LOAD) {
        int capacity = GROW_CAPACITY(table->capacity);
        adjustCapacity(table, capacity);
    }

    // Check if the entry already exists in table or not.
    Entry* entry = findEntry(table->entries, table->capacity, key);
    bool isNewKey = entry->key == NULL;

    // Act accordingly (don't count tombstones).
    if (isNewKey && IS_NIL(entry->value)) table->count++;

    entry->key = key;
    entry->value = value;
    return isNewKey;
}

bool tableDelete(Table* table, ObjString* key) {
    if (table->count == 0) return false;

    // Find the entry.
    Entry* entry = findEntry(table->entries, table->capacity, key);
    if (entry->key == NULL) return false;

    // Place a tombstone sentinel in the deleted entry's place.
    entry->key = NULL;
    entry->value = BOOL_VAL(true);
    return true;
}

void tableAddAll(Table* from, Table* to) {
    for (int i = 0; i < from->capacity; i++) {
        Entry* entry = from->entries + i;
        if (entry->key != NULL) {
            tableSet(to, entry->key, entry->value);
        }
    }
}

ObjString* tableFindString(
    Table* table,
    const char* chars,
    int length,
    uint32_t hash    
) {
    // Similar to findEntry, but with key differences!

    if (table->count == 0) return NULL;

    uint32_t index = hash % table->capacity;
    for (;;) {
        Entry* entry = table->entries + index;
        if (entry->key == NULL) {
            // Stop if we find an entry non-tombstone entry.
            if (IS_NIL(entry->value)) return NULL;
        } else if (
            entry->key->length == length
            && entry->key->hash == hash
            && memcmp(entry->key->chars, chars, length) == 0
        ) {
            // We found it.
            return entry->key;
        }

        index = (index + 1) % table->capacity;
    }
}