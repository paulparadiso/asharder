import RPi.GPIO as GPIO

class LED:

    def __init__(self):
        self.led_pin = 6
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.led_pin, 1)

    def off(self):
        GPIO.output(self.led_pin, 0)