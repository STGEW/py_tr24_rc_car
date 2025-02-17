# Installation of Micropython interpreter to the Raspberry pi PICO W

1) Download an fw from the website https://micropython.org/download/RPI_PICO_W/. I'll download a version 1.24.1
2) Interpreter can be uploaded in the same way as a 'normal' fw. Hold BOOTSEL btn and connect usb cable. You'll see a directory is mounted into your FS
3) just drag and drop a firmware to that directory.
4) Disconnect the cable

That's it. Micropython is running on the MCU

# Uploading Micropython code to the MCU

For that you need a python utility <strong>mpremote</strong>. Install it with a command: <strong>pip install mpremote</strong>

Also the driver for NRF from a standard library is used. I'm mentioning the commit '68e3e07' just to share the version which I used at that particular moment of time.

```
git clone https://github.com/micropython/micropython-lib.git
git checkout 68e3e07
cd micropython-lib/micropython/drivers/radio/nrf24l01
mpremote a1 cp ./nrf24l01.py :
```

Or you can assign the path to the directory <strong>micropython-lib</strong> to a variable <strong>$MICROLIB_PAT</strong> and use it later.

## useful commands
```
pip install mpremote
mpremote --help
mpremote a1
```

To remove files from the MCU use the command:
```
mpremote a0 rm your_file_1.py your_file_2.py
```

## Car
```
mpremote a0 cp ../consts.py : && \
mpremote a0 cp ../rf_task.py : && \
mpremote a0 cp main.py : && \
mpremote a0 cp utils.py : && \
mpremote a0 cp motor_driver_task.py : 
mpremote a0 cp $MICROLIB_PATH/micropython/drivers/radio/nrf24l01/nrf24l01.py :
```

## RC
```
mpremote a0 cp ../consts.py : && \
mpremote a0 cp ../rf_task.py : && \
mpremote a0 cp main.py : && \
mpremote a0 cp joystick_task.py : 
mpremote a0 cp $MICROLIB_PATH/micropython/drivers/radio/nrf24l01/nrf24l01.py :
```
