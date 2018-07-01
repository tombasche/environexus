import logging

import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.light import Light, PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['environexus==1.0']

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Awesome Light platform."""
    try:
        import environexus
    except ImportError as ex:
        logging.exception('Failed to import lib: {}'.format(ex))

    # Assign configuration variables. The configuration check takes care they are
    # present.
    host = config.get(CONF_HOST)

    # Setup connection with devices/cloud
    hub = environexus.LightHub(host)

    # Add devices
    add_devices(NexusNeroLight(light) for light in hub.lights)


class NexusNeroLight(Light):
    """Representation of an Awesome Light."""

    def __init__(self, light):
        """Initialize an AwesomeLight."""
        self._light = light
        self._name = light.name
        self._state = light.current_status

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.
        """
        self._light.turn_on()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.turn_off()

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._light.current_status
