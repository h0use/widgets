import logging
import time
import socket

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ikettle'
DEPENDENCIES = []

TCP_PORT = 2000
BUFFER_SIZE = 10
INITIATE = b"HELLOKETTLE\n"

BUTTON_100 = b'set sys output 0x80\n' # Select 100C button
BUTTON_95 = b'set sys output 0x2' # Select 95C button
BUTTON_80 = b'set sys output 0x4000' # Select 80C button
BUTTON_65 = b'set sys output 0x200' # Select 65C button
BUTTON_WARM = b'set sys output 0x8' # Select Warm button
BUTTON_WARM_5 = b'set sys output 0x8005' # Warm option is 5 mins
BUTTON_ON = b'set sys output 0x4' # Select On button
BUTTON_OFF = b'set sys output 0x0' # Turn off

def setup(hass, config):
    # Get the host from the configuration. Use DEFAULT_TEXT if no name is provided
    host = config[DOMAIN].get('host', '127.0.0.1')

    s = initiate(host)

    # Send some commands to prove this works
    s.send(BUTTON_ON)
    time.sleep(1)
    s.send(BUTTON_95)
    s.send(BUTTON_OFF)

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', host)

    return True

def initiate(self, host):
    # Open a connection to the kettle
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, TCP_PORT))
    s.send(INITIATE)

    return s
