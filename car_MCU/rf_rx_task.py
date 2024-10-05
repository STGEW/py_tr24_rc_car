from consts import CE_PIN, CSN_PIN, SCK_PIN, MOSI_PIN, MISO_PIN
from consts import UNDER_DEBUG

from machine import Pin, SPI
from nrf24l01 import NRF24L01
import struct



if UNDER_DEBUG:
    pass
else:
    csn = Pin(CSN_PIN, mode=Pin.OUT, value=1)
    ce = Pin(CE_PIN, mode=Pin.OUT, value=0)
    spi = SPI(0, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN), baudrate=400000)
    nrf = NRF24L01(spi, csn, ce, payload_size=32)
    nrf.set_channel(124)

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2

def init_rf_rx_task():
    print("Init RF RX task")
    if UNDER_DEBUG:
        pass
    else:
        pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
        nrf.open_tx_pipe(pipes[0])
        nrf.open_rx_pipe(1, pipes[1])
        nrf.start_listening()


def run_rf_rx_task():
    if UNDER_DEBUG:
        return None, None
    else:
        if nrf.any():
            # print(f"Something is coming")
            while nrf.any():
                buf = nrf.recv()
                j_x, j_y = struct.unpack("ii", buf)
                print(f"received joystick x: {j_x} y: {j_y}")
                return j_x, j_y
        else:
            # print(f'nothing to receive')
            return None, None
