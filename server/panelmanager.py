from emum import Enum

class PanelState(Enum):
    LOOPING = 1
    RECORDING = 2
    PLAYBACK = 3

class PanelManager:

    def __init__(self, callback):
        self.panelState = PanelState.LOOPING
        self.callback = callback

    def button_pressed(button):
        if button == 'random':
            pass
        if button == 'record':
            pass
        if button == 'play':
            pass
        if button == 'save':
            pass
        if button == 'erase':
            pass
        if button == 'send':
            pass