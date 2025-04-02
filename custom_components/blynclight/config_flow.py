from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN  # Import from const.py

class BlynclightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Blynclight", data={"host": user_input["host"]})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host", default="http://192.168.1.x:5000"): str
            }),
            errors={}
        )
        