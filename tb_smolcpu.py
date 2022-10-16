from amaranth.sim import Simulator
from smolcpu import smolcpu

dut = smolcpu()
def bench():
    for state in range(256):
        yield

sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("smolcpu.vcd"):
    sim.run()
