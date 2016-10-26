import logging
import time
import socket

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ikettle'
DEPENDENCIES = []

TCP_PORT = 2000
BUFFER_SIZE = 10
INITIATE = b"HELLOKETTLE\n"

SET_STRING = 'set sys output 0x'

BUTTON_100 = '80' # Select 100C button
BUTTON_95 = '2' # Select 95C button
BUTTON_80 = '4000' # Select 80C button
BUTTON_65 = '200' # Select 65C button
BUTTON_WARM = '8' # Select Warm button
BUTTON_WARM_5 = '8005' # Warm option is 5 mins
BUTTON_ON = '4' # Select On button
BUTTON_OFF = '0' # Turn off

def setup(hass, config):
    # Get the host from the configuration. Use DEFAULT_TEXT if no name is provided
    host = config[DOMAIN].get('host', '127.0.0.1')

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', host)

    s = initiate(host)

    def press_button_on(call):
        s.send( button_code(BUTTON_ON) )

    def press_button_off(call):
        s.send( button_code(BUTTON_OFF) )

    def press_button_100(call):
        s.send( button_code(BUTTON_100) )

    hass.services.register(DOMAIN, 'press_button_on', press_button_on)
    hass.services.register(DOMAIN, 'press_button_off', press_button_off)
    hass.services.register(DOMAIN, 'press_button_100', press_button_100)

    return True

def initiate(host):
    # Open a connection to the kettle
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, TCP_PORT))
    s.send(INITIATE)

    return s

def button_code(button):
    return (SET_STRING + button + '\n').encode()
