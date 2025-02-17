from consts import Driver

DRIVER_MAX_VALUE = 65535
DRIVER_COEF = DRIVER_MAX_VALUE / 100

DEAD_ZONE = 200
DEAD_ZONE_START = 2048 - DEAD_ZONE
DEAD_ZONE_END = 2048 + DEAD_ZONE
TURN_COEF = 0.60    # this coefficient is chosen after several experiments
ADC_TO_PERCENTAGE = 100.0 / 2048.0


def conv_joy_to_engines_pwr(j_x, j_y, pwr):
    """
    Convert joystick values to engines pwr (-100..100) for each side
    Arguments:
        j_x (0...4096) - x axis from joystick
        j_y (0...4096) - y axis from joystick
        pwr (EnginesPwr) - engines pwr class
    """

    turn = 0
    forward = 0

    if j_x >= DEAD_ZONE_START and j_x <= DEAD_ZONE_END:
        forward = 0
    else:
        forward = j_x
        # centering
        forward -= 2048

    if j_y >= DEAD_ZONE_START and j_y <= DEAD_ZONE_END:
        turn = 0
    else:
        turn = j_y
        # centering
        turn -= 2048

    forward = forward * ADC_TO_PERCENTAGE
    turn = turn * ADC_TO_PERCENTAGE
  

    pwr.left = forward
    pwr.right = forward

    if turn > 0:
        #  turn to the right. Left wheels should rotate faster
        pwr.left += turn * TURN_COEF
        pwr.right -= turn * TURN_COEF
    elif turn < 0:
        # turn to the left. Right wheels should rotate faster than left
        pwr.left -= -1 * turn * TURN_COEF
        pwr.right += -1 * turn * TURN_COEF

    # limit within -100..100 range 
    pwr.left = max(-100, min(100, pwr.left))
    pwr.right = max(-100, min(100, pwr.right))


def conv_engines_pwr_to_driver(pwr, d):
    """
    Converts engines pwr to driver data structure
    Arguments:
        pwr (EnginesPwr) - engines pwr class
        d (Driver) - can be applied to driver directly
    """
    def helper(e):
        if e == 0:
            direction = Driver.OFF
            duty = 0
        elif e > 0:
            direction = Driver.FORWARD
            duty = e * DRIVER_COEF
        elif e < 0:
            direction = Driver.REVERSE
            duty = -1 * e * DRIVER_COEF
        return int(duty), direction

    d.duty_cycle_A, d.direction_A = helper(pwr.left)
    d.duty_cycle_B, d.direction_B = helper(pwr.right)

