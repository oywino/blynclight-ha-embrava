import aiohttp
from homeassistant.components.light import LightEntity, SUPPORT_COLOR
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_ON, STATE_OFF

DOMAIN = "blynclight"

RGB_TO_ACTION = {
    (255, 0, 0): "red",
    (0, 150, 0): "green",
    (0, 0, 150): "blue"
}
ACTION_TO_RGB = {v: k for k, v in RGB_TO_ACTION.items()}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Blynclight light from a config entry."""
    host = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BlyncLightEntity(hass, host, entry.entry_id)])

class BlyncLightEntity(LightEntity):
    def __init__(self, hass: HomeAssistant, host: str, entry_id: str):
        self.hass = hass
        self._host = host
        self._state = STATE_OFF
        self._rgb_color = (0, 0, 0)
        self._unique_id = f"blynclight_{entry_id}"
        self._name = "Blynclight"

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def is_on(self):
        return self._state == STATE_ON

    @property
    def rgb_color(self):
        return self._rgb_color

    @property
    def supported_features(self):
        return SUPPORT_COLOR

    async def async_turn_on(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            if "rgb_color" in kwargs:
                r, g, b = kwargs["rgb_color"]
                action = RGB_TO_ACTION.get((r, g, b), "blue")
            else:
                action = "blue"
            data = {"action": action}
            await session.post(self._host, json=data)
            self._state = STATE_ON
            self._rgb_color = ACTION_TO_RGB.get(action, (0, 0, 150))

    async def async_turn_off(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            data = {"action": "off"}
            await session.post(self._host, json=data)
            self._state = STATE_OFF
            self._rgb_color = (0, 0, 0)

    async def async_update(self):
        pass
