from machine import ADC, UART, Pin
import os

from consts import X_AXIS_PIN, Y_AXIS_PIN
from consts import BOOT_LED_PIN, RADIO_LED_PIN

from rf_task import init_rf, run_rf_tx


adc_x = ADC(Pin(X_AXIS_PIN)) # 0-65535
adc_y = ADC(Pin(Y_AXIS_PIN)) # 0-65535


class MainLoop:

    def __init__(self):
        self._uart0 = UART(
            0, baudrate=460800, tx=Pin(0), rx=Pin(1))
        os.dupterm(self._uart0, 0)

        self.boot_led = Pin(BOOT_LED_PIN, Pin.OUT)
        self.boot_led.value(1)

        self.radio_led = Pin(RADIO_LED_PIN, Pin.OUT)
        self.radio_led.value(0)

        init_rf()

    def run(self):
        while True:
            self._loop()

    def _loop(self):
        x = adc_x.read_u16()
        y = adc_y.read_u16()
        print(f'joystick: {x} {y}')
        res = run_rf_tx(x, y)
        if res:
            self.radio_led.value(1)
        else:
            self.radio_led.value(0)


ml = MainLoop()
ml.run()
