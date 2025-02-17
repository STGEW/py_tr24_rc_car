from consts import CE_PIN, CSN_PIN, SCK_PIN, MOSI_PIN, MISO_PIN
from consts import PIPES
from consts import RF_CHANNEL, RF_PAYLOAD

from machine import Pin, SPI
from nrf24l01 import NRF24L01
import struct

csn = Pin(CSN_PIN, mode=Pin.OUT, value=1)
ce = Pin(CE_PIN, mode=Pin.OUT, value=0)
spi = SPI(0, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))
nrf = NRF24L01(spi, csn, ce, payload_size=RF_PAYLOAD)
nrf.set_channel(RF_CHANNEL)


def init_rf():
    nrf.open_tx_pipe(PIPES[0])
    nrf.open_rx_pipe(1, PIPES[1])
    nrf.start_listening()


def run_rf_rx():
    if nrf.any():
        # print(f"Something is coming")
        buf = nrf.recv()
        j_x, j_y = struct.unpack("ii", buf)
        return j_x, j_y
    else:
        # print(f'nothing to receive')
        return None, None


def run_rf_tx(x, y):
    res = False
    try:
        nrf.send(struct.pack("ii", x, y))
        print(f"Something was send x: {x} y: {y}")
        res = True
    except OSError:
        print("OS error")
        pass
    return res
