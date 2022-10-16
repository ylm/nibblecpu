from amaranth import *
from enum import IntEnum
from full_adder import *

class Operations(IntEnum):
    NOP = 0
    ADD = 1
    ADC = 2
    SUB = 3
    SBB = 4
    OR  = 5
    AND = 6
    XOR = 7

class ALU(Elaboratable):
    def __init__(self):

        self.carry_in = Signal()
        self.operandX = Signal(4)
        self.operandY = Signal(4)
        '''
        self.operation = Signal(Operations)
        '''
        self.carry = Signal()
        self.overflow = Signal()
        self.zero = Signal()
        self.result = Signal(4)
        self.dummy = Signal()

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self.dummy.eq(~self.dummy)
        full_adder_cascade = Array((FullAdder() for idx in range(4)))
        m.submodules.full_adder0 = full_adder_cascade[0]
        m.submodules.full_adder1 = full_adder_cascade[1]
        m.submodules.full_adder2 = full_adder_cascade[2]
        m.submodules.full_adder3 = full_adder_cascade[3]
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
            m.d.comb += self.result[idx].eq(full_adder_cascade[idx].sum)
        m.d.comb += self.zero.eq(~(self.result.any()))
        m.d.comb += self.overflow.eq(full_adder_cascade[2].carry_out ^ full_adder_cascade[3].carry_out)
        '''
        with m.Switch(self.operation):
            with m.Case(Operations.ADD):
                m.d.comb += self.result.eq(self.operandX + self.operandY)
        '''
        return m
