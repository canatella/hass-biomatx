"""Common properties for BiomatX entities."""
import typing

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .bus import BiomatxDevice
from .const import _LOGGER, BIOMATX_SIGNAL_UPDATE, DOMAIN


class BiomatxEntity(Entity):
    """Base entity."""

    def __init__(self, device: BiomatxDevice):
        """Initialize a BiomatX entity."""
        super().__init__()

        self.biomatx_device = device

    @property
    def should_poll(self) -> bool:
        """Hass should not poll."""
        return False

    @property
    def unique_id(self) -> typing.Union[str, None]:
        """Return a unique ID."""
        return f"{self.biomatx_device.module.address}_{self.biomatx_device.address}"

    @property
    def name(self) -> str:
        """Return a name."""
        return self.unique_id
    
    @property
    def device_info(self):
        """Return the device info."""
        return {"identifiers": {(DOMAIN, self.unique_id)}, "name": self.name}

    @callback
    def updated(self):
        _LOGGER.debug(f"updating {repr(self.biomatx_device)}")
        self.async_write_ha_state()
        
    async def async_added_to_hass(self):
        """Call when entity is added to hass."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                BIOMATX_SIGNAL_UPDATE.format(
                    self.biomatx_device.__class__.__name__, self.biomatx_device.module.address, self.biomatx_device.address
                ),
                self.updated,
            )
        )
        self.updated()

