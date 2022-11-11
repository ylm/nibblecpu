# SPDX-License-Identifier: BSD-2-Clause
import sys
from amaranth.sim import Simulator
from amaranth.back import verilog
from smolcpu import smolcpu

sys.setrecursionlimit(100000)

test_prg = [
        0x924, #MOV R2, 4
        0x9C5, #MOV JSR, 5
        0x042, #DSZ R2
        0xFFD, #JR -3
        0xFFB, #JR -5
        0x142, #ADD R4, R2
        0x0E0, #RET 0
        0xFF9, #JR -7
        0xFFE, #JR -02
        0x040, #DSZ R0
        0x030, #DEC R0
        0x300, #SUB R0, R0
        0x020, #INC R0
        0x040, #DSZ R0
        0xF00, #JR  01
        0x020, #INC R0
        0x016, #ADD R0, 6
        0xFFF] #JR -01
dut = smolcpu(test_prg)
ports = [
        dut.pc, dut.opcode, dut.error
        ]
print("making verilog")
with open("smolcpu.v","w") as f:
    f.write(verilog.convert(dut, ports=ports))
