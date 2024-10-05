from consts import FORWARD, OFF, REVERSE, BRAKE
from consts import AI1_PIN, AI2_PIN, BI1_PIN, BI2_PIN
from consts import STBY_PIN
from consts import PWM_A_PIN, PWM_B_PIN
from consts import UNDER_DEBUG

from machine import Pin, PWM


if UNDER_DEBUG:
    AI1_gpio = None
    AI2_gpio = None
    BI1_gpio = None
    BI2_gpio = None

    STBY_gpio = None

    A_pwm = None
    B_pwm = None

else:
    AI1_gpio = Pin(AI1_PIN, Pin.OUT)
    AI2_gpio = Pin(AI2_PIN, Pin.OUT)
    BI1_gpio = Pin(BI1_PIN, Pin.OUT)
    BI2_gpio = Pin(BI2_PIN, Pin.OUT)

    STBY_gpio = Pin(STBY_PIN, Pin.OUT)

    A_pwm = PWM(Pin(PWM_A_PIN))
    A_pwm.freq(50)
    A_pwm.duty_u16(0)

    B_pwm = PWM(Pin(PWM_B_PIN))
    B_pwm.freq(50)
    B_pwm.duty_u16(0)


def init_motor_driver_task():
    if UNDER_DEBUG:
        return
    _set_motor_direction(AI1_gpio, AI2_gpio, OFF)
    _set_motor_direction(BI1_gpio, BI2_gpio, OFF)
    STBY_gpio.on()


def run_motor_driver_task(driver):
    # print(f'Run motor driver task. Driver: {driver.direction_A} {driver.direction_B} {driver.duty_cycle_A} {driver.duty_cycle_B}')
    if UNDER_DEBUG:
        return
    _set_motor_direction(AI1_gpio, AI2_gpio, driver.direction_A)
    A_pwm.duty_u16(driver.duty_cycle_A)
    _set_motor_direction(BI1_gpio, BI2_gpio, driver.direction_B)
    B_pwm.duty_u16(driver.duty_cycle_B)


def _set_motor_direction(i1_pin, i2_pin, direction):
    # print(f'i1: {i1_pin} i2: {i2_pin}, direction: {direction}')
    if direction == FORWARD:
        i1_pin.on()
        i2_pin.off()
    elif direction == OFF:
        i1_pin.off()
        i2_pin.off()
    elif direction == REVERSE:
        i1_pin.off()
        i2_pin.on()
    else:
        # BRAKE
        i1_pin.on()
        i2_pin.on()