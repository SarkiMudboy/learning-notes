import math


"""
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

    if n % 2 > 0:
        for i in range(math.floor(math.sqrt(n)), 0, -1):
            if n % i == 0:
                if i == n:
                    continue
                return n / i


if __name__ == "__main__":

    print(gcd(48, 36))
