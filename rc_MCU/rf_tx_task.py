
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

def init_rf_tx_task():
    if UNDER_DEBUG:
        print("Init RF TX task")
    else:
        pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
        nrf.open_tx_pipe(pipes[1])
        nrf.open_rx_pipe(1, pipes[0])
        nrf.stop_listening()


def run_rf_tx_task(x, y):
    if UNDER_DEBUG:
        return True

    res = False
    try:
        nrf.send(struct.pack("ii", x, y))
        # nrf.send_start(struct.pack("ii", x, y))
        print(f"Something was send x: {x} y: {y}")
        res = True
    except OSError:
        print("OS error")
        pass
    return res
