from enum import Enum

class PanelState(Enum):
    LOOPING = 1
    RECORDING = 2
    PLAYBACK = 3

class PanelManager:

    def __init__(self, callback):
        self.panel_state = PanelState.LOOPING
        self.callback = callback

    def button_pressed(self, button):
        if button == 'random':
            if self.panel_state == PanelState.LOOPING:
                self.callback({'command': 'randomFile'})
                return
            if self.panel_state == PanelState.PLAYBACK:
                self.callback({'command': 'stopPlayback'})
                self.callback({'command': 'randomFile'})
                self.panel_state = PanelState.LOOPING
                return
        if button == 'record':
            if self.panel_state == PanelState.LOOPING:
                self.callback({'command': 'startRecording'})
                self.panel_state = PanelState.RECORDING
                return
            if self.panel_state == PanelState.RECORDING:
                self.callback({'command': 'stopRecording'})
                self.panel_state = PanelState.PLAYBACK
                return
            if self.panel_state == PanelState.PLAYBACK:
                self.callback({'command': 'startRecording'})
                self.panel_state = PanelState.RECORDING
                return
        if button == 'play':
            if self.panel_state == PanelState.LOOPING:
                self.callback({'command': 'playLoop'})
                return
            if self.panel_state == PanelState.RECORDING:
                self.callback({'command': 'stopRecording'})
                self.callback({'command': 'playRecording'})
                self.panel_state = PanelState.PLAYBACK
                return
            if self.panel_state == PanelState.PLAYBACK:
                self.callback({'command': 'playRecording'})
                return
        if button == 'save':
            if self.panel_state in (PanelState.RECORDING, PanelState.PLAYBACK):
                self.callback({'command': 'saveRecording'})
                return
        if button == 'erase':
            if self.panel_state in (PanelState.RECORDING, PanelState.PLAYBACK):
                self.callback({'command': 'eraseRecording'})
                return
        if button == 'send':
            if self.panel_state in (PanelState.RECORDING, PanelState.PLAYBACK):
                self.callback({'command': 'sendRecording'})
                return

    def get_panel_state():
        return self.panel_state