import logging
import platform
import subprocess as sp

import voluptuous as vol

from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv

#REQUIREMENTS = ['ikettle_api']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    ip_address = config.get(CONF_HOST)

    add_devices([ikettle_power(hass, ip_address)])

class ikettle_power(SwitchDevice):

    def __init__(self, hass, ip_address):
        # from ikettle_api import iKettle

        self._hass = hass
        self._ip_address = ip_address
        self._state = False
        self._ikettle = iKettle(ip_address)
        self.update()

    @property
    def name(self):
        return 'ikettle_onoff'

    @property
    def is_on(self):
        return self._state

    def turn_on(self):
        self._ikettle.press_button_on()
        self._state = True

    def turn_off(self):
        self._ikettle.press_button_off()
        self.update()
        return self._state

    def update(self):
        #self._ikettle.get_state('On')


class iKettle():

    BUFFER_SIZE = 10

    BUTTON_WARM = '8' # Select Warm button
    BUTTON_WARM_5 = '8005' # Warm option is 5 mins

    BUTTON_ON = '4' # Select On button
    BUTTON_OFF = '0' # Turn off
    BUTTON_100 = '80' # Select 100C button
    BUTTON_95 = '2' # Select 95C button
    BUTTON_80 = '4000' # Select 80C button
    BUTTON_65 = '200' # Select 65C button

    # First is the button code, second is complementary to status code
    BUTTONS = {
        '100': [0x80, 0x20],
        '95': [0x2, 0x10],
        '80': [0x4000, 0x8],
        '65': [0x200, 0x4],
        'On': [0x4, 0x1]
    }


    def __init__(self, host):
        self.host = host

    def _initiate(self):
        import time
        import socket

        # Open a connection to the kettle
        TCP_PORT = 2000
        INITIATE = b"HELLOKETTLE\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, TCP_PORT))
        s.send(INITIATE)
        return s

    def _button_code(button):
        SET_STRING = 'set sys output 0x'
        return (SET_STRING + button + '\n').encode()

    def _send_message(self, message):
        s = self._initiate()
        s.send(message)
        reply = s.recv(4096)
        s.close()
        return reply

    def get_state(self, button):
        data = self._send_message('get sys status\n'.encode())
        if (data.startswith("sys status key=")):
            if (len(data)<16):
                key = 0
            else:
                key = ord(data[15]) & 0x3f
        state = (key & BUTTONS[button][1] != 0)


    def press_button_on(self):
        self._send_message(iKettle._button_code(self.BUTTON_ON))

    def press_button_off(self):
        self._send_message(iKettle._button_code(self.BUTTON_OFF))

    def press_button_100(self):
        self._send_message(iKettle._button_code(self.BUTTON_100))

    def press_button_95(self):
        self._send_message(iKettle._button_code(self.BUTTON_95))

    def press_button_80(self):
        self._send_message(iKettle._button_code(self.BUTTON_80))

    def press_button_65(self):
        self._send_message(iKettle._button_code(self.BUTTON_65))
