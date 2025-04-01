#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct dll_node {
    struct dll_node* prev;
    struct dll_node* next;
    char* string;
} dll_node;

typedef struct dll {
    dll_node* first_node;
    dll_node* last_node;
} dll;

dll* dll_new();
void dll_destroy(dll*);

void dll_insert(dll*, char[]);
int dll_find(dll*, char[]); /* Corresponding to index? */
void dll_delete(dll*, char*);

int main() {
    dll* list = dll_new();
    dll_insert(list, "Hejsan!");
    dll_insert(list, "Hejdå!");
    dll_delete(list, "Hejsan!");
    dll_insert(list, "Bajs!");
    printf("%s\n", list->last_node->string);
    printf("%s\n", list->first_node->next->string);
    printf("%s\n", list->last_node->prev->string);

    printf("%d\n", strcmp("Hejsan!", list->first_node->string));
}

void dll_insert(dll* list, char* string) {
    if (list) {
        /* Create new node. */
        char* new_string = malloc(strlen(string) + 1);
        strcpy(new_string, string);
        dll_node* new_node = malloc(sizeof(dll_node));
        *new_node = (dll_node) {
            .prev = list->last_node,
            .next = NULL,
            .string = new_string
        };

        /* Make list point to it. */
        list->last_node = new_node;
        if (!list->first_node) {
            list->first_node = new_node;
        } else {
            list->first_node->next = new_node;
        }
    }
}

void dll_delete(dll* list, char* string) {
    if (list) {
        dll_node* current = list->first_node;
        while (current->next) {
            if (!strcmp(current->string, string)) {
                printf("Found!");
                current->prev->next = current->next;
                current->next->prev = current->prev;

                free(current->string);
                free(current);
            }
            current = current->next;
        }
    }
}

dll* dll_new() {
    dll* ret = malloc(sizeof(dll));

    *ret = (dll) {
        .first_node = NULL,
        .last_node = NULL,
    };

    return ret;
}

void dll_destroy(dll* target) {
    free(target); /* Need to travers and free the dynamically allocated strings. */
}