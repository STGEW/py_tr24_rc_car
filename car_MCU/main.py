from machine import UART, Pin
import os
from time import ticks_diff, ticks_ms
import utime

from consts import ML_PERIOD_MSEC, ML_SLEEP_MSEC, RF_TIMEOUT_MSEC
from consts import Driver, EnginesPwr
from consts import BOOT_LED_PIN, RADIO_LED_PIN

from motor_driver_task import init_motor_driver_task, run_motor_driver_task
from rf_task import init_rf, run_rf_rx

from utils import conv_joy_to_engines_pwr, conv_engines_pwr_to_driver


class MainLoop:

    def __init__(self):
        self._uart0 = UART(
            0, baudrate=460800, tx=Pin(0), rx=Pin(1))
        os.dupterm(self._uart0, 0)

        self.cur_t = ticks_ms()
        self.last_t = self.cur_t - ML_PERIOD_MSEC
        self.last_rx_t = self.cur_t - RF_TIMEOUT_MSEC

        self.driver = Driver()
        self.eng_power = EnginesPwr()

        self.boot_led = Pin(BOOT_LED_PIN, Pin.OUT)
        self.boot_led.value(1)

        self.radio_led = Pin(RADIO_LED_PIN, Pin.OUT)
        self.radio_led.value(0)

        init_rf()
        init_motor_driver_task()

    def run(self):
        while True:
            self.cur_t = ticks_ms()
            diff_t = ticks_diff(self.cur_t, self.last_t)
            if diff_t > ML_PERIOD_MSEC:
                self._loop()
                self.last_t = ticks_ms()
            else:
                utime.sleep_ms(ML_SLEEP_MSEC)

    def _loop(self):
        # receive from joystick
        j_x, j_y = run_rf_rx()
        if j_x is not None and j_y is not None:
            self.last_rx_t = ticks_ms()
            self.radio_led.value(1)
            conv_joy_to_engines_pwr(j_x, j_y, self.eng_power)
            conv_engines_pwr_to_driver(self.eng_power, self.driver)
            print(
                f'Received joystick x: {j_x} y: {j_y}; '
                f'Engine pwr: {self.eng_power.left} {self.eng_power.right}; '
                f'Driver: {self.driver.direction_A} {self.driver.direction_B} '
                f'{self.driver.duty_cycle_A} {self.driver.duty_cycle_B}')
        if self._timeout_protection():
            self.radio_led.value(0)

        run_motor_driver_task(self.driver)

    def _timeout_protection(self):
        """
        Protects us from losing the connection to RC
        """
        if ticks_diff(self.cur_t, self.last_rx_t) > RF_TIMEOUT_MSEC:
            print("Timeout protection")
            self.driver.direction_A = Driver.OFF
            self.driver.direction_B = Driver.OFF
            self.driver.duty_cycle_A = 0
            self.driver.duty_cycle_B = 0
            return True
        else:
            # print("!!!NO Timeout protection")
            return False


ml = MainLoop()
ml.run()
