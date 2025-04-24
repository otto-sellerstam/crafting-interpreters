#include <stdlib.h>
#include <stdio.h>

int main() {
    char myString[] = "123 345";

    char* end;

    printf("%g\n", strtod(myString, &end));
    printf("End points to '%c'\n", *end);
}