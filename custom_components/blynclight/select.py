import aiohttp
import logging
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)

DOMAIN = "blynclight"
OPTIONS = ["red", "green", "blue", "off"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Blynclight select entity from a config entry."""
    host = hass.data[DOMAIN][entry.entry_id]
    entity = BlyncLightSelectEntity(hass, host, entry.entry_id)
    async_add_entities([entity])

class BlyncLightSelectEntity(SelectEntity):
    def __init__(self, hass: HomeAssistant, host: str, entry_id: str):
        """Initialize the Blynclight select entity."""
        self.hass = hass
        self._host = host
        self._attr_unique_id = f"blynclight_{entry_id}"
        self._attr_name = "Blynclight"
        self._attr_options = OPTIONS
        self._attr_current_option = "off"  # Initial state: no-color
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "Blynclight",
            "manufacturer": "Embrava",
            "model": "Blynclight Plus"
        }

    @callback
    def _handle_option_change(self):
        """Handle option change and update HA state."""
        self.async_write_ha_state()

    async def async_select_option(self, option: str):
        """Handle selection of an option."""
        if option not in OPTIONS:
            _LOGGER.error(f"Invalid option: {option}")
            return
        _LOGGER.debug(f"Selecting option: {option}")
        async with aiohttp.ClientSession() as session:
            data = {"action": option}
            await session.post(self._host, json=data)
            self._attr_current_option = option
            self._handle_option_change()

    async def async_update(self):
        """No polling needed; state is set by user actions."""
        pass
