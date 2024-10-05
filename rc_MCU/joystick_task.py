from consts import X_AXIS_PIN, Y_AXIS_PIN
from machine import ADC, Pin


adc_x = ADC(Pin(X_AXIS_PIN)) # 0-65535
adc_y = ADC(Pin(Y_AXIS_PIN)) # 0-65535


def run_joystick_task():
    # micropython returns us 16 bits value. However
    # since I want to share us much logic as I can with C code
    # it's easier to convert it ti 12 bits (in C we have 12 bits from ADC)
    # and to keep all the originally designed conversions
    x = convert_16bit_to_12bit(adc_x.read_u16())
    y = convert_16bit_to_12bit(adc_y.read_u16())
    return x, y


def convert_16bit_to_12bit(adc_value_16bit):
    # Ensure the input is within the 16-bit range
    if adc_value_16bit < 0 or adc_value_16bit > 65535:
        raise ValueError("ADC value must be in the range 0-65535")

    # Scale the 16-bit value to a 12-bit range
    adc_value_12bit = int((float(adc_value_16bit) / 65535.0) * 4095.0)

    return adc_value_12bit
