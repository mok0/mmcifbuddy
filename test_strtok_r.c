/*
  C program to demonstrate working of stamdart C library function
  strtok_r() by splitting string based on space character.
*/
#include <stdio.h>
#include <string.h>

int main()
{
  char str[] = "1     2  3 . ? ATOM 1.2 3.4      5.6";
  char* token;
  char* rest = str;

  while ((token = strtok_r(rest, " ", &rest)))
    printf(">%s<\n", token);

  return 0;
}
