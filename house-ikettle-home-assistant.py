import logging
import time
import socket

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ikettle'
DEPENDENCIES = []

TCP_PORT = 2000
BUFFER_SIZE = 10
INITIATE = "HELLOKETTLE\n"
COMMAND_START = "set sys output 0x4\n"
COMMAND_95 = "set sys output 0x2\n"
COMMAND_WARM = "set sys output 0x8\n"

def setup(hass, config):
    # Get the host from the configuration. Use DEFAULT_TEXT if no name is provided
    host = config[DOMAIN].get('host', '127.0.0.1')

    # Open a connection to the kettle
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, TCP_PORT))
    s.send(bytes(INITIATE))
    time.sleep(1)
    s.send(bytes(TEMP))

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', host)



    return True
