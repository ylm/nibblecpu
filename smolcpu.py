# LICENSE AND COPYRIGHT GOES HERE...

from amaranth import *
from alu import ALU
from enum import IntEnum

class Registers(IntEnum):
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7
    R8 = 8
    R9 = 9
    OUT= 10
    IN = 11
    JSR= 12
    PCL= 13
    PCM= 14
    PCH= 15

class smolcpu(Elaboratable):

    def __init__(self, prg_bin=None):

        #ports
        self.pc = Signal(12)
        self.instruction = Signal(12)
        self.opcode = Signal(4)
        self.operandX = Signal(4)
        self.operandY = Signal(4)
        self.page = Signal(4)
        self.out = Signal(4)
        self.inr = Signal(4)
        self.jsr = Signal(4)
        self.carry = Signal()
        self.overflow = Signal()
        self.zero = Signal()
        self.sp = Signal(3)
        self.displacement = Signal(signed(8))
        self.source_inv = Signal()
        self.prg_bin = prg_bin
        self.comb_pc = Signal(12)
        self.error = Signal()

    def elaborate(self, platform):
        m = Module()
        data_memory = Array((Signal(4) for idx in range(256)))
        #data_memory = Array([Signal(4) for idx in range(10)] + [self.out] + [self.inr] + [self.jsr] + [self.pc[0:4]] + [self.pc[4:8]] + [self.pc[8:12]] + [Signal(4) for idx in range(256-16)])

        program_mem = Memory(width=12, depth=2**16, init=self.prg_bin)
        read_program = program_mem.read_port()
        m.submodules.read_program = read_program
        m.d.comb += [read_program.addr.eq(self.comb_pc),
                self.instruction.eq(read_program.data)]
        m.d.comb += self.opcode.eq(self.instruction[8:12])
        m.d.comb += self.operandX.eq(self.instruction[4:8])
        m.d.comb += self.operandY.eq(self.instruction[0:4])
        m.d.comb += self.comb_pc.eq(self.pc + self.displacement)

        alu = ALU()
        m.submodules.alu = alu
        m.d.comb += self.source_inv.eq(0)
        m.d.comb += alu.operandX.eq(Repl(self.source_inv,4) ^ data_memory[self.operandX])
        m.d.comb += alu.operandY.eq(data_memory[self.operandY])


        m.d.sync += self.pc.eq(self.comb_pc)
        m.d.sync += self.carry.eq(alu.carry)
        with m.If(self.opcode.any()):
            m.d.sync += self.overflow.eq(alu.overflow)

        m.d.comb += alu.carry_in.eq(0)
        m.d.comb += self.displacement.eq(1)
        with m.Switch(self.opcode):
            with m.Case(0): #extended instructions
                with m.Switch(self.operandX):
                    with m.Case(0): # CP R0, N
                        m.d.comb += alu.carry_in.eq(1)
                        m.d.comb += alu.operandX.eq(~self.operandY)
                        m.d.comb += alu.operandY.eq(data_memory[Registers.R0])
                        m.d.sync += self.zero.eq(~alu.ArithResult.any())
                    with m.Case(1): # ADD R0, N
                        m.d.comb += alu.operandX.eq(data_memory[Registers.R0])
                        m.d.comb += alu.operandY.eq(self.operandY)
                        m.d.sync += data_memory[Registers.R0].eq(alu.ArithResult)
                        m.d.sync += self.zero.eq(~alu.ArithResult.any())
                    with m.Case(2): # INC Ry
                        m.d.comb += alu.operandX.eq(0)
                        m.d.comb += alu.carry_in.eq(1)
                        m.d.sync += data_memory[self.operandY].eq(alu.ArithResult)
                        m.d.sync += self.carry.eq(self.carry)
                        m.d.sync += self.zero.eq(~alu.ArithResult.any())
                    with m.Case(3): # DEC Ry
                        m.d.comb += alu.operandX.eq(15)
                        m.d.comb += alu.carry_in.eq(0)
                        m.d.sync += data_memory[self.operandY].eq(alu.ArithResult)
                        m.d.sync += self.carry.eq(~alu.ArithResult.any())
                        m.d.sync += self.zero.eq(~alu.ArithResult.any())
                    with m.Case(4): # DSZ Ry
                        m.d.comb += alu.operandX.eq(15)
                        m.d.comb += alu.carry_in.eq(0)
                        m.d.sync += data_memory[self.operandY].eq(alu.ArithResult)
                        m.d.sync += self.carry.eq(self.carry)
                        m.d.sync += self.zero.eq(self.zero)
                        with m.If(~alu.ArithResult.any()):
                            m.d.comb += self.displacement.eq(2)
                    with m.Case(5): # OR R0, N
                        m.d.comb += alu.operandX.eq(data_memory[Registers.R0])
                        m.d.comb += alu.operandY.eq(self.operandY)
                        m.d.sync += data_memory[Registers.R0].eq(alu.OR_LogicResult)
                        m.d.sync += self.carry.eq(1)
                        m.d.sync += self.zero.eq(~alu.OR_LogicResult.any())
                    with m.Case(6): # AND R0, N
                        m.d.comb += alu.operandX.eq(data_memory[Registers.R0])
                        m.d.comb += alu.operandY.eq(self.operandY)
                        m.d.sync += data_memory[Registers.R0].eq(alu.ANDLogicResult)
                        m.d.sync += self.carry.eq(1)
                        m.d.sync += self.zero.eq(~alu.ANDLogicResult.any())
                    with m.Case(7): # XOR R0, N
                        m.d.comb += alu.operandX.eq(data_memory[Registers.R0])
                        m.d.comb += alu.operandY.eq(self.operandY)
                        m.d.sync += data_memory[Registers.R0].eq(alu.XORLogicResult)
                        m.d.sync += self.carry.eq(~self.carry)
                        m.d.sync += self.zero.eq(~alu.XORLogicResult.any())
                    #with m.Case(8): # EXR N
                    with m.Case(14): # RET R0, N
                        m.d.sync += data_memory[Registers.R0].eq(self.operandY)
                        m.d.sync += self.sp.eq(self.sp - 1)
                        m.d.comb += self.comb_pc.eq(Cat(data_memory[0x10+(3*self.sp)-3],Cat(data_memory[0x10+(3*self.sp)-2],data_memory[0x10+(3*self.sp)-1])))
                        with m.If(self.sp == 0):
                            m.d.sync += self.error.eq(1)

            with m.Case(1): # ADD
                m.d.sync += data_memory[self.operandX].eq(alu.ArithResult)
                m.d.sync += self.zero.eq(~alu.ArithResult.any())
            with m.Case(2): # ADC
                m.d.sync += data_memory[self.operandX].eq(alu.ArithResult)
                m.d.comb += alu.carry_in.eq(self.carry)
                m.d.sync += self.zero.eq(~alu.ArithResult.any())
            with m.Case(3): # SUB
                m.d.comb += self.source_inv.eq(1)
                m.d.sync += data_memory[self.operandX].eq(alu.ArithResult)
                m.d.comb += alu.carry_in.eq(1)
                m.d.sync += self.zero.eq(~alu.ArithResult.any())
            with m.Case(4): # SBB
                m.d.comb += self.source_inv.eq(1)
                m.d.sync += data_memory[self.operandX].eq(alu.ArithResult)
                m.d.comb += alu.carry_in.eq(~self.carry)
                m.d.sync += self.zero.eq(~alu.ArithResult.any())
            with m.Case(5): # OR
                m.d.sync += data_memory[self.operandX].eq(alu.OR_LogicResult)
                m.d.sync += self.zero.eq(~alu.OR_LogicResult.any())
            with m.Case(6): # AND
                m.d.sync += data_memory[self.operandX].eq(alu.ANDLogicResult)
                m.d.sync += self.zero.eq(~alu.ANDLogicResult.any())
            with m.Case(7): # XOR
                m.d.sync += data_memory[self.operandX].eq(alu.XORLogicResult)
                m.d.sync += self.zero.eq(~alu.XORLogicResult.any())
            with m.Case(8): # MOV RX, RY
                m.d.sync += data_memory[self.operandX].eq(data_memory[self.operandY])
                with m.If(self.operandX == Registers.PCL):
                    m.d.comb += self.comb_pc.eq(Cat(data_memory[self.operandY],Cat(data_memory[Registers.PCM],data_memory[Registers.PCH])))
                with m.If(self.operandX == Registers.JSR):
                    m.d.comb += self.comb_pc.eq(Cat(data_memory[Registers.JSR],Cat(data_memory[Registers.PCM],data_memory[Registers.PCH])))
                    m.d.sync += self.sp.eq(self.sp + 1)
                    m.d.sync += [data_memory[0x10+(3*self.sp)+0].eq((self.pc + 1).bit_select(0,4)),
                            data_memory[0x10+(3*self.sp)+1].eq((self.pc + 1).bit_select(4,4)),
                            data_memory[0x10+(3*self.sp)+2].eq((self.pc + 1).bit_select(8,4))]
                    with m.If(self.sp == 5):
                        m.d.sync += self.error.eq(1)
            with m.Case(9): # MOV
                m.d.sync += data_memory[self.operandX].eq(self.operandY)
                with m.If(self.operandX == Registers.PCL):
                    m.d.comb += self.comb_pc.eq(Cat(data_memory[Registers.PCL],Cat(data_memory[Registers.PCM],data_memory[Registers.PCH])))
                with m.If(self.operandX == Registers.JSR):
                    m.d.comb += self.comb_pc.eq(Cat(self.operandY,Cat(data_memory[Registers.PCM],data_memory[Registers.PCH])))
                    m.d.sync += self.sp.eq(self.sp + 1)
                    m.d.sync += [data_memory[0x10+(3*self.sp)+0].eq((self.pc + 1).bit_select(0,4)),
                            data_memory[0x10+(3*self.sp)+1].eq((self.pc + 1).bit_select(4,4)),
                            data_memory[0x10+(3*self.sp)+2].eq((self.pc + 1).bit_select(8,4))]
                    with m.If(self.sp == 5):
                        m.d.sync += self.error.eq(1)
            with m.Case(10): # MOV
                ind_addr = Cat(data_memory[self.operandY], data_memory[self.operandX])
                m.d.sync += data_memory[ind_addr].eq(data_memory[Registers.R0])
            with m.Case(11): # MOV
                ind_addr = Cat(data_memory[self.operandY], data_memory[self.operandX])
                m.d.sync += data_memory[Registers.R0].eq(data_memory[ind_addr])
            with m.Case(12): # MOV
                m.d.sync += data_memory[Cat(self.operandY, self.operandX)].eq(data_memory[0])
            with m.Case(13): # MOV
                m.d.sync += data_memory[Registers.R0].eq(data_memory[Cat(self.operandY, self.operandX)])
            with m.Case(14): # LPC
                m.d.sync += data_memory[14].eq(self.operandY)
                m.d.sync += data_memory[15].eq(self.operandX)
            with m.Case(15): # JR
                m.d.comb += self.displacement.eq(Cat(self.operandY, self.operandX) + 1)


        return m
