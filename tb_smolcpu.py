from amaranth.sim import Simulator
from smolcpu import smolcpu

test_prg = [
        0x020, #INC R0
        0xF00, #JR +00
        0x020, #INC R0
        0x020, #INC R0
        0x010, #ADD R0, 0
        0x015, #ADD R0, 5
        0x042, #DSZ R2
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
def bench():
    for state in range(256):
        yield

sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("smolcpu.vcd"):
    sim.run()
