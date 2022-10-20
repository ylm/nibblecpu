# SPDX-License-Identifier: BSD-2-Clause
from amaranth import *

class FullAdder(Elaboratable):
    def __init__(self):
        self.carry_in = Signal()
        self.carry_out = Signal()
        self.operand1 = Signal()
        self.operand2 = Signal()
        self.sum = Signal()
        self.dummy = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.sum.eq(self.carry_in ^ self.operand1 ^ self.operand2)
        m.d.comb += self.carry_out.eq((self.operand1 & self.operand2) | ((self.operand1 ^ self.operand2) & self.carry_in))
        m.d.sync += self.dummy.eq(~self.dummy)
        return m
