"""Manages light entities for the BiomatX integration."""
import biomatx

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER, DOMAIN
from .entity import BiomatxEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> bool:
    """Setups sensor entities."""
    bus = hass.data[DOMAIN][entry.entry_id]
    entities = [BiomatxSwitch(switch) for switch in bus.switches]
    _LOGGER.debug(f"setting up {len(entities)} BiomatX switches")
    async_add_entities(entities, True)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Tear down sensor entities."""
    return True


class BiomatxSwitch(BiomatxEntity, BinarySensorEntity):
    """BiomatX switch device."""

    def __init__(self, device: biomatx.Switch):
        """Initialize a sensor device."""
        super().__init__(device)

    @property
    def is_on(self):
        """Return true if switch is pressed."""
        return self.biomatx_device.pressed
