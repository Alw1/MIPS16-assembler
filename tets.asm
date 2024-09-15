# Token Testing
.data
.text
.globl
string: .asciiz "MIPS Assembly!"
number: .word 1234
	array: .word 1, 2, 3, 4
add addi addiu ADD
.text
.globl main

main:
    li $v0, 4          # Print string
    la $a0, string
    syscall

    li $v0, 1          # Print integer
    lw $a0, (number)
    syscall

    li $v0, 10         # Exit
    syscall


    0x09128

