#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exercise the AoE decoder through cooperative attach on the installed Rosetta."""
import os
from pathlib import Path
import subprocess
import sys

build = Path(sys.argv[1] if len(sys.argv) > 1 else 'build').resolve()
helper = build / 'bin/x87sidecar'
fixture = build / 'bin/tests/test_aoe_softfault'
symbols = {}
for line in subprocess.check_output(['nm', '-g', str(fixture)], text=True).splitlines():
    fields = line.split()
    if len(fields) == 3:
        symbols[fields[2]] = int(fields[0], 16)
env = dict(os.environ,
    AOE_SOFTFAULT_PC=hex(symbols['_aoe_softfault_begin']),
    AOE_SOFTFAULT_END=hex(symbols['_aoe_softfault_end']),
    AOE_SOFTFAULT_TARGET=hex(symbols['_aoe_softfault_handler']),
    AOE_SOFTFAULT_TARGET1=hex(symbols['_aoe_softfault_handler']),
    X87_STRICT_ALLOC='1')
subprocess.run([str(helper), '--cooperative', str(fixture)], env=env, check=True, timeout=30)
# The composed hook must also retain the generic decoder's aliases.
for name in ('test_decoder_fcomp_st', 'test_decoder_arpl'):
    # An unused range enables composition without matching these test executables.
    outside = dict(env, AOE_SOFTFAULT_PC='0x10000', AOE_SOFTFAULT_END='0x10010',
                   AOE_SOFTFAULT_TARGET='0x20000', AOE_SOFTFAULT_TARGET1='0x20010')
    subprocess.run([str(helper), '--cooperative', str(build / 'bin/tests' / name)],
                   env=outside, check=True, timeout=30)
