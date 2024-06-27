try:
    import RPi.GPIO as GPIO
except RuntimeError:
    import GPIO_nonpi as GPIO
import threading
import time

class LED:

    def __init__(self):
        self.led_pin = 6
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.led_pin, 1)

    def off(self):
        GPIO.output(self.led_pin, 0)

class Button:

    def __init__(self, pin_cb):
        self.record_pin = 15
        self.play_loop_pin = 5
        self.save_pin = 22
        self.send_pin = 23
        self.erase_pin = 27
        self.random_loop_pin = 4
        self.pin_list = [self.record_pin, self.play_loop_pin, self.save_pin, self.send_pin, self.erase_pin, self.random_loop_pin]
        self.pin_status = {}
        self.pin_fired = {}
        self.pin_status[self.record_pin] = 0
        self.pin_fired[self.record_pin] = False
        self.pin_status[self.play_loop_pin] = 0
        self.pin_fired[self.play_loop_pin] = False
        self.pin_status[self.save_pin] = 0
        self.pin_fired[self.save_pin] = False
        self.pin_status[self.send_pin] = 0
        self.pin_fired[self.send_pin] = False
        self.pin_status[self.erase_pin] = 0
        self.pin_fired[self.erase_pin] = False
        self.pin_status[self.random_loop_pin] = 0
        self.pin_fired[self.random_loop_pin] = False
        self.pin_names = {
            self.record_pin: 'record',
            self.play_loop_pin: 'play',
            self.save_pin: 'save',
            self.send_pin: 'send',
            self.erase_pin: 'erase',
            self.random_loop_pin: 'random'
        }
        self.pin_cb = pin_cb
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.record_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.play_loop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.save_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.send_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.erase_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.random_loop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def poll(self):
        while True:
            for pin in self.pin_list:
                v = GPIO.input(pin)
                if v == 0:
                    self.pin_status[pin] = 0
                    self.pin_fired[pin] = False
                else:
                    self.pin_status[pin] = self.pin_status + 1
                if (self.pin_status[pin] > 2) and (self.pin_fired[pin] == False):
                    self.pin_cb(self.pin_names[pin])
                    self.pin_fired[pin] = True
            time.sleep(0.1)


    def start_polling(self):
        self.thread = threading.Thread(target=self.poll, daemon=True)
        self.thread.start()

    
