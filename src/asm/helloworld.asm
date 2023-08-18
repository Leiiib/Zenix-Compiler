global _main         ; declare main() method
extern _printf       ; link to external library

section .data
    message: db "Hello, world!", 10, 0

section .text
_main:                    
    push message           ; save message to the stack
    call _printf           ; display the first value on the stack

    mov eax, 1
    mov ebx, 0
    int 0x80