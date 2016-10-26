import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ikettle'
DEPENDENCIES = []

DEFAULT_HOST = 127.0.0.1

def setup(hass, config):
    # Get the host from the configuration. Use DEFAULT_TEXT if no name is provided
    host = config[DOMAIN].get('host', DEFAULT_HOST)

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', str(host))

    return True
