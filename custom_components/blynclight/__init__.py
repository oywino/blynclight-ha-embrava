from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "blynclight"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Blynclight Embrava integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Blynclight from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data["host"]
    # Forward to the 'select' platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "select")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(entry, ["select"])
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
