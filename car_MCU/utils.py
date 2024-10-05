from time import ticks_diff, ticks_ms

from consts import DEAD_ZONE_START, DEAD_ZONE_END
from consts import TURN_COEF, DRIVER_COEF
from consts import FORWARD, OFF, REVERSE, BRAKE
from consts import ADC_TO_PERCENTAGE
from consts import RF_TIMEOUT_MSEC


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
            direction = OFF
            duty = 0
        elif e > 0:
            direction = FORWARD
            duty = e * DRIVER_COEF
        elif e < 0:
            direction = REVERSE
            duty = -1 * e * DRIVER_COEF
        return int(duty), direction

    d.duty_cycle_A, d.direction_A = helper(pwr.left)
    d.duty_cycle_B, d.direction_B = helper(pwr.right)


def timeout_protection(d, last_rf_rx_tick):
    """
    Protects us from losing the connection to RC
    Arguments:
    - d (Driver) - a class with driver data
    - last_rf_rx_tick - a msec tick when last RF package
       was received
    """
    cur_tick = ticks_ms()
    # print(f"Cur: {cur_tick} last: {last_rf_rx_tick}")
    if ticks_diff(cur_tick, last_rf_rx_tick) > RF_TIMEOUT_MSEC:
        # print("Timeout protection")
        d.direction_A = OFF
        d.direction_B = OFF
        d.duty_cycle_A = 0
        d.duty_cycle_B = 0
        return True
    else:
        # print("!!!NO Timeout protection")
        return False
