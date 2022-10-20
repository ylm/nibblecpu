# NibbleCPU

An [Amaranth](https://amaranth-lang.org/docs/amaranth/latest/intro.html) implementation of [Voja Antonic's 4bit CPU](https://hackaday.io/project/182568-badge-for-2020-supercon-years-of-lockdown).

This CPU was developed for the Hackaday Supercon 2020, but was put on hold until Supercon 2022.

It has great documentation - see the [hackaday.io page](https://hackaday.io/project/182568-badge-for-2020-supercon-years-of-lockdown).

# Competition

Matt Venn [announced a competition](https://twitter.com/matthewvenn/status/1581277116561489921) to build an RTL version of the CPU (it's emulated on a PIC microchip), with the intent to run on an FPGA or create an ASIC version.

# Setup

* install Amaranth: pip install amaranth
* run the testbench: python tb_smolcpu.py

# Streams

The HDL was developed on these streams:

* https://www.twitch.tv/videos/1625230564
* https://www.twitch.tv/videos/1625940867
* https://www.twitch.tv/videos/1628488048

# License

[BSD 2-Clause License](LICENSE)
