from time import ticks_diff, ticks_us
from machine import UART, Pin
import os

from consts import UNDER_DEBUG
from consts import BOOT_LED_PIN
from consts import RC_LOOP_PERIOD_USEC
from consts import RADIO_LED_PIN

from joystick_task import run_joystick_task
from rf_tx_task import init_rf_tx_task, run_rf_tx_task

# not esp
# TBD: move to pins constants
uart0 = UART(0, baudrate=460800, tx=Pin(0), rx=Pin(1))
# esp
# uart0 = UART(2, baudrate=115200, timeout_char=100)
radio_led_pin = None


def init_uart():
    os.dupterm(uart0, 0)
    pass


def init_boot_led():
    boot_led_pin = Pin(BOOT_LED_PIN, Pin.OUT)
    boot_led_pin.value(1)


def init_radio_led():
    global radio_led_pin
    radio_led_pin = Pin(RADIO_LED_PIN, Pin.OUT)
    radio_led_pin.value(0)


def init():
    print(f'Run init')
    init_boot_led()
    init_radio_led()
    init_uart()
    init_rf_tx_task()


def loop():
    last_t = ticks_us()
    x, y = run_joystick_task()
    # x, y = 2000, 3000
    if UNDER_DEBUG:
        data = uart0.readline()
        if data:
            # print(f"Read from UART data: {data}")
            x, y = data.decode('utf-8').split(' ')
            x = int(x)
            y = int(y)
    # print(f'joystick: {x} {y}')
    res = run_rf_tx_task(x, y)
    if res:
        radio_led_pin.value(1)
    else:
        radio_led_pin.value(0)
    return last_t


def main():
    init()
    # variable to track loop call
    last_t = ticks_us()

    while True:
        cur_t = ticks_us()
        last_t = loop()
        # if ticks_diff(cur_t, last_t) > RC_LOOP_PERIOD_USEC:
        #     last_t = loop()

main()
