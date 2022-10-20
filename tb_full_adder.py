# SPDX-License-Identifier: BSD-2-Clause
from amaranth.sim import Simulator
import full_adder

dut = full_adder.FullAdder()
def bench():
    for state in range(8):
        yield dut.carry_in.eq(state & 1)
        yield dut.operand1.eq((state & 2)>>1)
        yield dut.operand2.eq((state & 4)>>2)
        yield
        yield dut.carry_out
        yield dut.sum
        #print("carry is ", dut.carry_out.as_unsigned(), " sum is ", dut.sum.as_unsigned())
        #assert (dut.carry_out == (dut.carry_in + dut.operand1 + dut.operand2))
    yield

sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("full_adder.vcd"):
    sim.run()
