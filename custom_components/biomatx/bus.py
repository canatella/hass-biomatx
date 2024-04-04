"""BiomatX bus utilities."""

import typing

import biomatx

from asyncio import gather
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import _LOGGER, BIOMATX_SIGNAL_UPDATE

BiomatxDevice = typing.Union[biomatx.Relay, biomatx.Switch]


class BiomatxBus(biomatx.Bus):
    """BiomatX bus wrapper."""

    def __init__(self, hass: HomeAssistant, module_count: int, serial_wait: float, all_off_address: int):
        """Initialize the bus."""
        super().__init__(module_count, serial_wait)
        self.hass = hass
        self.all_off_address = all_off_address
        self.port = None
        

    async def callback(self, what: BiomatxDevice):
        """Dispatch events."""
        _LOGGER.debug(f"{repr(what)} has been updated")
        async_dispatcher_send(
            self.hass,
            BIOMATX_SIGNAL_UPDATE.format(what.__class__.__name__, what.module.address, what.address),
        )

    async def connect(self, port: str):
        """Connect to the RS485 port."""
        self.port = port
        await super().connect(port, self.callback)
        await self.reset()

    async def send_all_off(self):
        """Turn all relays off using the scenario."""
        if not self.all_off_address:
            _LOGGER.warning(
                "all off scenario not configured, unable to turn all relays off."
            )

        await self.scenarios.switches[self.all_off_address].activate()

    async def all_off(self, *args):
        tasks = [self.send_all_off()]
        for relay in self.relays:
            if relay.on:
                relay.force_toggle()
                tasks.append(self.callback(relay))
        await gather(*tasks)
                
    async def reset(self, *args):
        """Make it so that the physical relay states match the in memory state.

        This works by using a scenario to turn everything off and then trigger the relay that should be on one by one.
        """
        if not self.all_off_address:
            _LOGGER.warning("all off scenario not configured, unable to reset.")

        await self.send_all_off()
        [await relay.switch.activate() for relay in self.relays if relay.on]


    async def reload(self, *args):
        await self.stop()
        await self.connect(self.port)
