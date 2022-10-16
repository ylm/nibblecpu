# LICENSE AND COPYRIGHT GOES HERE...

from amaranth import *

class smolcpu(Elaboratable):

    def __init__(self):

        #ports
        self.pc = Signal(12)
        self.opcode = Signal(4)
        self.operandX = Signal(4)
        self.operandY = Signal(4)
        self.page = Signal(4)
        self.out = Signal(4)
        self.in = Signal(4)
        self.jsr = Signal(4)

    def elaborate(self, platform):
        m = Module()

        program_mem = Memory(width=12, depth=2**16)
        read_program = program_mem.read_port()

        register_file = Array((Signal(4, name = f'r{idx}' for idx in range(10))), self.out, self.in, self.jsr, self.pc[0:4], self.pc[4:8], self.pc[8:12])

        m.submodules.read_program = read_program

        return m
