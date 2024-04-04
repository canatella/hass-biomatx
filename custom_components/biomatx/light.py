"""Manages light entities for the BiomatX integration."""
import biomatx

from asyncio import Lock
from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER, DOMAIN
from .entity import BiomatxEntity

lock = Lock()

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> bool:
    """Setups light entities."""
    bus = hass.data[DOMAIN][entry.entry_id]
    entities = [BiomatxLight(relay) for relay in bus.relays]
    _LOGGER.debug(f"setting up {len(entities)} BiomatX lights")
    async_add_entities(entities, True)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Tear down light entities."""
    return True


class BiomatxLight(BiomatxEntity, LightEntity):
    """BiomatX light device."""

    def __init__(self, device: biomatx.Relay):
        """Initialize a light device."""
        super().__init__(device)


    @property
    def is_on(self):
        """Return true if light is on."""
        return self.biomatx_device.on

    async def async_turn_on(self, **kwargs):
        """Turn device on."""
        _LOGGER.debug(f"waiting to turn {self} on")
        async with lock:
            _LOGGER.debug(f"turning {self} on")
            if self.is_on:
                return

            await self.biomatx_device.toggle()
            
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn device off."""
        _LOGGER.debug(f"waiting to turn {self} off")
        async with lock:
            _LOGGER.debug(f"turning {self} off")

            if not self.is_on:
                return

            await self.biomatx_device.toggle()
            
        self.async_write_ha_state()

    def reset(self):
        """Set the physical to the assumed state."""
        self.biomatx_device.force_toggle()
