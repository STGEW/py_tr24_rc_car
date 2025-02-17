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

RF_CHANNEL = 124
RF_PAYLOAD = 32

# joysticks
X_AXIS_PIN = 26
Y_AXIS_PIN = 27

# Main loop
# 50 MSEC -> 20 Hz
ML_PERIOD_MSEC = 50
ML_SLEEP_MSEC = 5
RF_TIMEOUT_MSEC = 500

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
PIPES = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

class Driver:
    FORWARD = 1
    OFF = 2
    REVERSE = 3
    BRAKE = 4

    def __init__(self):
        self.direction_A = self.OFF
        self.direction_B = self.OFF
        self.duty_cycle_A = 0
        self.duty_cycle_B = 0

class EnginesPwr:
    def __init__(self):
        # values are in range -100 ... 100
        self.left = 0        
        self.right = 0
