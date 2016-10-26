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

    s = initiate(host)

    # Send some commands to prove this works
    s.send( (SET_STRING + BUTTON_ON + '\n').encode() )
    time.sleep(1)
    s.send( (SET_STRING + BUTTON_95 + '\n').encode() )
    time.sleep(1)
    s.send( (SET_STRING + BUTTON_OFF + '\n').encode() )

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', host)

    return True

def initiate(host):
    # Open a connection to the kettle
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, TCP_PORT))
    s.send(INITIATE)

    return s
