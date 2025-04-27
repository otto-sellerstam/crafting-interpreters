#include <stdio.h>

typedef struct {
    int a;
} Base;

typedef struct {
    Base b;
    int c;
} Child;

int main() {
    Base b = { .a = 3};
    Child c = { .b = b, .c = 4 };

    printf("%d\n", *(int*)&c);
    printf("%d\n", *((int*)&c + 1));
}