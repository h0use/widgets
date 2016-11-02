import logging
import platform
import subprocess as sp

import voluptuous as vol

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
import homeassistant.helpers.config_validation as cv

CONF_IP_ADDRESS = 'ip_address'

DEFAULT_NAME = 'iKettle'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP_ADDRESS): cv.string
})

def setup_platform(hass, config, add_devices, discover_info=None):
    ip_address = config.get(CONF_IP_ADDRESS)

    add_devices([iKettle(hass, ip_address)])

class iKettle(SwitchDevice):

    def __init__(self, hass, ip_address):
        import ikettle_api

        self._hass = hass
        self._ip_address = ip_address
        self._state = False
        self._ikettle = ikettle_api.iKettle(ip_address)

    @property
    def is_on(self):
        return self._state

    def turn_on(self):
        self._ikettle.press_button_on()
