import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ikettle'
DEPENDENCIES = []

def setup(hass, config):
    # Get the host from the configuration. Use DEFAULT_TEXT if no name is provided
    host = config[DOMAIN].get('text', 'alternative text')

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', 'test')

    return True
