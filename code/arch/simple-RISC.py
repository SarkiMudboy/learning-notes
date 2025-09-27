from typing import List, Any, Optional, Tuple
import math


def numOfRotations():
    """
    In some cases, we can rotate an integer to the right by n positions (less than or
    equal to 31) so that we obtain the same number. For example: a 8-bit number 11011011 can
    be right rotated by 3 or 6 places to obtain the same number. Write an assembly program to
    efficiently count the number of ways we can rotate a number to the right such that the result
    is equal to the original number.

    simple-RISC ->

        .loop:
            add r3, r3, 1 @ count += 1
            and r2, r1, 1 @ iso last bit
            lsl r2, r2, 31 @ shift the bit to the MSB pos
            or r1, r1, r2 @ prepend the og val with isod bit
            cmp r0, r1 @ compare og with test val
            beq .evaluate
            lsr r1, r1, 1 @ shift the last bit to the right
            b .loop

        .evaluate:
            mod r6, r4, r3 @ 31 % k
            cmp r6, 0 @ (31 % k) > 0?
            bgt .end
            div r5, r4, r3 @ 31 // k
            mov r6, r5 @ result = (n/d)

        .end:
            mov r6, 0 @ not synmetric

    """
    ...


# Compute the cubic armstrong of a number i.e. 153^3 == 1^3 + 5^3 + 3^15.3
# div num by 10 i.e. 15.3 <- 3 is tens
# by 100 1.53 <- hundreds


def computeArmstrong(number: int) -> bool:
    """

    A number is known as a cubic Armstrong number if the sum of the cubes of
    the decimal digits is equal to the number itself. For example, 153 is a cubic Armstrong number
    (153 = 13 + 53 + 33). You are given a number n, and it is known to be between 1
    and 1 million. Can you write a piece of code to find out if this number
    is a cubic Armstrong number. Return true if it is a cubic Armstrong number; otherwise, return false.

    Args:
        number -> integer between (1 - 1_000_000) which is to be tested

    Returns:
        bool -> True if it passes and False if it fails the test

    simple-RISC: -> Arr -> Ox12345678 (64 -bit) Lil Endian [(Ox78563421)], [...] x -> (loc * 4 + i)

    .main:
        mov r1, 0       @ (index for arr)
        mov r4, r1      @ store index for reuse
        mov r0, val     @ (value to test)
        call .test
    .test:
        mov r2, r0,          @ temp_number = number
        b .loop
    .continue:
        cmp r4, r1           @ for i in digits
        bgt .end
        beq .end
        ld r5, [loc * 4]r4   @ i
        mov r7, r5
        call .cube           @ i ** 3
        add r6, r6, r7       @ sum([i ** 3 for i in digits])
        add r4, r4, 4
    .end:
         cmp r6, r0    @ sum([i ** 3 for i in digits]) == number
         beq .isArm
         b isNotArm
    .isArm:
        mov r1, 1
        ret
    .isNotArm:
        mov r1, 0
        ret
    .loop:
        cmp r2, 0            @ while temp_num > 0
        bgt .continue
        beq .continue
        mod r3, r2, 10       @ temp_num % 10
        st r3, [(loc * 4)]r1 @ digits.append(temp_num % 10)
        div r2, r2, 10       @ temp_num = temp_num // 10
        add r1, r1, 4
        b .loop

    .cube:
        mul r8, r7, r7
        mul r7, r8, r7
        ret
    """

    digits = []
    temp_num = number

    while temp_num > 0:

        digits.append(temp_num % 10)
        temp_num = temp_num // 10

    # reverse to get correct order

    digits.reverse()

    return sum([i**3 for i in digits]) == number


def gcd(num1: int, num2: int) -> int:
    """
    simple-RISC:

    .gcd: @ assuming r1, r2 = num1, num2
        mov r0, 0 @ divisor = 0
        mod r3, r1, 2 @ num1 % 2
        cmp r3, 0 @ if num1 % 2 > 0
        bgt .baseCase1
        mod r3, r2, 2 @ num2 % 2
        cmp r3, 0 @ if num2 % 2 > 0
        bgt .baseCase2

    .continue:
        // move stuff to stack here...

        sub sp, sp, 8 /* create space on the stack */
        st r0, [sp] /* store r0 (divisor) */

        sub sp, sp, 8
        st r1, [sp] /* store r1 (num1) */

        sub sp, sp, 8
        st r2, [sp] /* store r2 (num2) */

        st ra 4[sp] @ push return address register

        div r1, r1, 2 @ num1 // 2
        div r2, r2, 2 @ num2 // 2
        call .gcd @ gcd(num1 // 2, num2 // 2) # assuming result is in r0

        // restore stack

        ld ra 4[sp] @ pop return address from the stack

        ld r2, [sp] /* load r2 (num2) */
        add sp, sp, 8

        ld r1, [sp] /* load r1 (num1) */
        add sp, sp, 8

        ld r0, [sp] /* load r0 (divisor) */
        add sp, sp, 8

        mul r0, r0, 2 @ 2 * gcd(num1 // 2, num2 // 2)
        b .found

    .baseCase1:
        // stack ...
        st ra 4[sp] @ push return address register
        mov r1, r1
        call .find_largest_divisor @ find_largest_divisor(num1) # rem to decrement stack pointer, result is in r0
        // restore stack
        ld ra 4[sp] @ pop return address from the stack
        mod r3, r2, r0 @ num2 % divisor
        cmp r3, 0 @  num2 % divisor == 0
        beq .found
        b .continue

    .baseCase2:
        // stack ...
        st ra 4[sp] @ push return address register
        mov r1, r2
        call .find_largest_divisor @ find_largest_divisor(num1) # rem to decrement stack pointer, result is in r0
        // restore stack
        ld ra 4[sp] @ pop return address from the stack
        mod r3, r1, r0 @ num1 % divisor
        cmp r3, 0 @  num2 % divisor == 0
        beq .found
        b .continue

    .found:
        ret
    """

    divisor = 0

    # base cases
    if num1 % 2 > 0:
        divisor = find_largest_divisor(num1)
        if num2 % divisor == 0:
            return divisor

    if num2 % 2 > 0:
        divisor = find_largest_divisor(num2)
        if num1 % divisor == 0:
            return divisor

    return 2 * gcd(num1 // 2, num2 // 2)


def find_largest_divisor(n: int) -> int:
    """
    simple-RISC:

    .find_largest_divisor:
        mod r2, r1, 2 @ n % 2
        cmp r2, 0 @ if n % 2 > 0
        bgt .continue_loop
        ret
    .continue_loop:
        // find out code for math.sqrt and math.floor
        call .bin_sqrt
        sub r5, r5, 1 @ -1
        cmp r5, 0 @ math.sqrt(n) > 0
        ...
        mod r4, r2, r3 @ n % i
        cmp r4, 0 @ if n % i == 0
        beq .continue
        ret
    .continue:
        cmp r2, r3 @ if i == n
        beq .continue_loop @ continue
        div r0, r2, r3 @ caller agrees on r0 as return register value
        ret

    """
    if n % 2 > 0:
        for i in range(math.floor(math.sqrt(n)), 0, -1):
            if n % i == 0:
                if i == n:
                    continue
                return n / i


def bin_sqrt(num: int) -> int:
    """

    simple-RISC -> assuming num is in register r0 and result is in r5

    mov r2, 2 @ prep to compare with num
    cmp r2, r0  @ if num < 2
    bgt .end

    mov r1 , 1 @ left = 1
    mov r2, r0 @ right = num
    mov r5, 0 @ result = 0
    b .loop

    .loop:
        cmp r1, r2 @ while left <= right
        bgt .found
        add r3, r1, r2 @ left = right
        div r3, r3, 2 @ (left + right) // 2
        mul r4, r3, r3 @ mid * mid
        cmp r0, r4 @ if mid * mid == num
        beq .midResult
        bgt .upper
        sub r2, r3, 1
        b .loop

    .upper:
        mov r5, r3
        add r1, r3, 1
        b .loop

    .midResult:
        mov r5, r3
        b.found

    .end:
        mov r5, r0
        b .found @ return num

    .found:
        ret @ return

    """

    if num < 2:
        return num

    left = 1
    right = num

    result = 0  # closest so far

    while left <= right:

        mid = (left + right) // 2

        if mid * mid == num:
            return mid
        elif (mid * mid) < num:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result


if __name__ == "__main__":
    print(bin_sqrt(52))
    # print(gcd(48, 36))
