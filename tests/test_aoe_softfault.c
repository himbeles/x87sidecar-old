/* SPDX-License-Identifier: MIT
 * Run with scripts/test_aoe_softfault.py: these bytes are invalid in 64-bit mode. */
#include <stdio.h>

volatile unsigned aoe_softfault_calls;
__attribute__((noinline)) void aoe_softfault_handler(void) { ++aoe_softfault_calls; }
extern void aoe_softfault_pair(void);
extern void aoe_softfault_single(void);

__asm__(".text\n"
        ".globl _aoe_softfault_begin\n"
        "_aoe_softfault_begin:\n"
        ".globl _aoe_softfault_pair\n"
        "_aoe_softfault_pair:\n"
        ".byte 0xd5, 0x7f\n" /* AAD: two-byte lowering. */
        "ret\n"
        ".globl _aoe_softfault_single\n"
        "_aoe_softfault_single:\n"
        ".byte 0x1e\n"       /* PUSH DS: one-byte lowering. */
        "ret\n"
        ".globl _aoe_softfault_end\n"
        "_aoe_softfault_end:\n");

int main(void)
{
    double sum;
    aoe_softfault_pair();
    aoe_softfault_single();
    __asm__ volatile("fld1; fld1; faddp; fstpl %0" : "=m"(sum) : : "st");
    if (aoe_softfault_calls != 2 || sum != 2.0) {
        printf("FAIL AoE decoder: calls=%u, sum=%g\n", aoe_softfault_calls, sum);
        return 1;
    }
    puts("PASS AoE one/two-byte software faults and x87 composition");
    return 0;
}
