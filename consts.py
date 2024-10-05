######### CONSTANTS

# Motor states
FORWARD = 1
OFF = 2
REVERSE = 3
BRAKE = 4

# Motor driver
DRIVER_MAX_VALUE = 65535
DRIVER_COEF = DRIVER_MAX_VALUE / 100

######## PINS

# motor driver pins
AI1_PIN = 6
AI2_PIN = 7
BI1_PIN = 8
BI2_PIN = 9
STBY_PIN = 10
PWM_A_PIN = 11
PWM_B_PIN = 12

RADIO_LED_PIN = 13

BOOT_LED_PIN = 15

# nrf24l01
SCK_PIN = 18
MOSI_PIN = 19
MISO_PIN = 16
CE_PIN = 20
CSN_PIN = 21


# joysticks
X_AXIS_PIN = 26
Y_AXIS_PIN = 27


# conversions:
DEAD_ZONE = 200
DEAD_ZONE_START = 2048 - DEAD_ZONE
DEAD_ZONE_END = 2048 + DEAD_ZONE
TURN_COEF = 0.60    # this coefficient is chosen after several experiments
ADC_TO_PERCENTAGE = 100.0 / 2048.0


# general
LOOP_PERIOD_USEC = 50000
RC_LOOP_PERIOD_USEC = 100000
RF_TIMEOUT_MSEC = 1500
UNDER_DEBUG = False


# shared data types:
class Driver:
    direction_A = OFF
    direction_B = OFF
    duty_cycle_A = 0
    duty_cycle_B = 0


class EnginesPwr:
    left = 0        # left -100 ... 100
    right = 0       # right -100 ... 100
