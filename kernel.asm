bits 16
org 0x7C00

start:
    ; --- Kernel Code ---
    jmp $ ; Infinite loop

section .data
    x dd 5

times 510-($-$$) db 0
dw 0xAA55