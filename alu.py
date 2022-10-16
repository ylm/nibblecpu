from amaranth import *
from enum import IntEnum
from full_adder import *

class ALU(Elaboratable):
    def __init__(self):

        self.carry_in = Signal()
        self.operandX = Signal(4)
        self.operandY = Signal(4)
        self.carry = Signal()
        self.overflow = Signal()
        self.ArithResult = Signal(4)
        self.OR_LogicResult = Signal(4)
        self.ANDLogicResult = Signal(4)
        self.XORLogicResult = Signal(4)
        self.dummy = Signal()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self.dummy.eq(~self.dummy)
        full_adder_cascade = Array((FullAdder() for idx in range(4)))
        for subm in full_adder_cascade:
            m.submodules += subm
        # Connecting the carry chain
        m.d.comb += [full_adder_cascade[0].carry_in.eq(self.carry_in),
                full_adder_cascade[1].carry_in.eq(full_adder_cascade[0].carry_out),
                full_adder_cascade[2].carry_in.eq(full_adder_cascade[1].carry_out),
                full_adder_cascade[3].carry_in.eq(full_adder_cascade[2].carry_out),
                self.carry.eq(full_adder_cascade[3].carry_out)]
        for idx in range(4):
            m.d.comb += [full_adder_cascade[idx].operand1.eq(self.operandX[idx]),
                    full_adder_cascade[idx].operand2.eq(self.operandY[idx])]

        for idx in range(4):
            m.d.comb += self.ArithResult[idx].eq(full_adder_cascade[idx].sum)

        m.d.comb += self.OR_LogicResult.eq(self.operandX | self.operandY)
        m.d.comb += self.ANDLogicResult.eq(self.operandX & self.operandY)
        m.d.comb += self.XORLogicResult.eq(self.operandX ^ self.operandY)

        m.d.comb += self.overflow.eq(full_adder_cascade[2].carry_out ^ full_adder_cascade[3].carry_out)
        return m
