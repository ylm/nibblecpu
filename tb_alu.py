from amaranth.sim import Simulator
from alu import ALU

dut = ALU()
def bench():
    yield dut.carry_in.eq(0)
    for state in range(256):
        yield dut.operandX.eq((state & 15))
        yield dut.operandY.eq((state & 240)>>4)
        yield
        yield dut.carry
        yield dut.ArithResult
        yield dut.zero
        yield dut.overflow
        #print("carry is ", dut.carry_out.as_unsigned(), " sum is ", dut.sum.as_unsigned())
        #assert (dut.carry_out == (dut.carry_in + dut.operand1 + dut.operand2))
    yield

sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("alu.vcd"):
    sim.run()
