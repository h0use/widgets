import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ikettle'
DEPENDENCIES = []

CONF_TEXT = 'text'
DEFAULT_TEXT = 'no text'

def setup(hass, config):
    # Get the text from the configuration. Use DEFAULT_TEXT if no name is provided
    text = config[DOMAIN].get(CONF_TEXT, DEFAULT_TEXT)

    # States are set in the format DOMAIN.OBJECT_ID
    hass.states.set('ikettle.iKettle', text)

    return True
