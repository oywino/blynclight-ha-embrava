"""Update entity for Blynclight Embrava integration."""
import json
import logging
from pathlib import Path

import aiohttp
from homeassistant.components.update import UpdateEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Blynclight update entity from a config entry."""
    async_add_entities([BlynclightUpdateEntity(hass)])

class BlynclightUpdateEntity(UpdateEntity):
    """Representation of a Blynclight update entity."""

    _attr_has_entity_name = True
    _attr_name = "Blynclight Update"

    def __init__(self, hass):
        """Initialize the update entity."""
        self._hass = hass
        self._attr_unique_id = f"{DOMAIN}_update"
        self._attr_title = "Blynclight Embrava"
        # Dynamically read the installed version from manifest.json
        manifest_path = Path(__file__).parent / "manifest.json"
        try:
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            self._attr_installed_version = manifest["version"]
        except Exception as err:
            _LOGGER.error(f"Failed to read manifest.json: {err}")
            self._attr_installed_version = "unknown"
        self._attr_latest_version = None

    async def async_update(self):
        """Fetch the latest version from GitHub."""
        session = async_get_clientsession(self._hass)
        try:
            async with session.get(
                "https://api.github.com/repos/oywino/blynclight-ha-embrava/releases/latest"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self._attr_latest_version = data["tag_name"].lstrip("v")
                else:
                    _LOGGER.warning(f"GitHub API returned {response.status}")
                    self._attr_latest_version = self._attr_installed_version
        except Exception as err:
            _LOGGER.error(f"Failed to fetch latest version: {err}")
            self._attr_latest_version = self._attr_installed_version

    @property
    def available(self):
        """Return if entity is available."""
        return self._attr_latest_version is not None
        