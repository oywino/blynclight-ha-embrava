import aiohttp
from homeassistant.components.light import LightEntity, SUPPORT_COLOR
from homeassistant.const import STATE_ON, STATE_OFF

DOMAIN = "blynclight"
DEFAULT_HOST = "http://windows-pc-ip:5000"  # Replace with your Windows PC IP

# Map RGB to actions (based on Embrava Connect hotkeys)
RGB_TO_ACTION = {
    (255, 0, 0): "red",    # Red
    (0, 150, 0): "green",  # Green (Embrava’s value)
    (0, 0, 150): "blue"    # Blue (Embrava’s value)
}
ACTION_TO_RGB = {v: k for k, v in RGB_TO_ACTION.items()}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    host = config.get("host", DEFAULT_HOST)
    async_add_entities([BlyncLightEntity(hass, host)])

class BlyncLightEntity(LightEntity):
    def __init__(self, hass, host):
        self.hass = hass
        self._host = host
        self._state = STATE_OFF
        self._rgb_color = (0, 0, 0)
        self._unique_id = "blynclight_embrava"
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
                action = RGB_TO_ACTION.get((r, g, b), "blue")  # Default to blue
            else:
                action = "blue"  # Default if no color specified
            data = {"action": action}
            await session.post(self._host, json=data)
            self._state = STATE_ON
            self._rgb_color = ACTION_TO_RGB.get(action, (0, 0, 150))  # Update local state

    async def async_turn_off(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            data = {"action": "off"}
            await session.post(self._host, json=data)
            self._state = STATE_OFF
            self._rgb_color = (0, 0, 0)

    async def async_update(self):
        # Local state tracking only; no status polling from Embrava Connect
        pass