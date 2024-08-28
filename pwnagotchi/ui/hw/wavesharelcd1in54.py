import logging

import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.hw.base import DisplayImpl


class Wavesharelcd1in54(DisplayImpl):
    def __init__(self, config):
        super(Wavesharelcd1in54, self).__init__(config, 'wavesharelcd1in54')

    def layout(self):
        fonts.setup(10, 8, 10, 45, 25, 9)
        self._layout['width'] = 240
        self._layout['height'] = 240
        self._layout['face'] = (0, 50)
        self._layout['name'] = (162, 72)
        self._layout['channel'] = (0, 5)
        self._layout['aps'] = (33, 5)
        self._layout['uptime'] = (170, 5)
        self._layout['line1'] = [0, 20, 240, 20]
        self._layout['line2'] = [0, 220, 240, 220]
        self._layout['friend_face'] = (55, 25)
        self._layout['friend_name'] = (95, 27)
        self._layout['shakes'] = (0, 225)
        self._layout['mode'] = (210, 225)
        self._layout['status'] = {
            'pos': (15, 130),
            'font': fonts.status_font(fonts.Medium),
            'max': 35
        }
        return self._layout

    def initialize(self):
        logging.info("initializing waveshare 1.54 inch lcd display")
        from pwnagotchi.ui.hw.libs.waveshare.lcd.lcdhat1in54.LCD_1inch54 import LCD_1inch54
        # self._display = LCD_1inch54()
        self._display = LCD_1inch54(rst=27, dc=22, bl=18) # for Spotspear lcdhat1.54inch
        self._display.Init()
        self._display.clear()
        self._display.bl_DutyCycle(50)

    def render(self, canvas):
        # self._display.ShowImage(canvas)
        rgb_im = canvas.convert('RGB')
        self._display.ShowImage(rgb_im)

    def clear(self):
        self._display.clear()
