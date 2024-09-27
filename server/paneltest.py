from panelmanager import PanelManager
from GPIO import LED, Button
import time

led = LED()

def callback(command):
    global led
    print(command)
    if command["command"] == "startRecording":
        led.on()
    if command["command"] == "stopRecording":
        led.off()

def main():
    panel_manager = PanelManager(callback)
    buttons = Button(panel_manager.button_pressed)
    buttons.start_polling()
    while True:
        time.sleep(1.0)

if __name__ == '__main__':
    main()