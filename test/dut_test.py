import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

# Define the test function
@cocotb.test()
async def apb_base_test(dut):
    # Create a clock with a period of 10 time units
    clock = Clock(dut.pclk, 10, units="ns")
    cocotb.fork(clock.start())

    # Reset the dut
    dut.rst_n <= 0
    await RisingEdge(dut.pclk)
    dut.rst_n <= 1
    await RisingEdge(dut.pclk)

    # Write some data to the pwdata signal
    dut.pwdata <= 123
    dut.psel <= 1
    dut.penable <= 1
    dut.pwrite <= 1

    # Wait for a rising edge of pclk
    await RisingEdge(dut.pclk)

    # Read the data from prdata signal
    dut.psel <= 1
    dut.penable <= 1
    dut.pwrite <= 0
    await RisingEdge(dut.pclk)
    prdata = dut.prdata.value

    # Print the read data
    print(f"Read data: {prdata}")

# Run the test
def run_sim():
    cocotb.regression.add(apb_base_test)
    cocotb.regression.report_pass()

run_sim()
