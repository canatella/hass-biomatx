"""Constants for the BiomatX integration."""

import logging

_LOGGER = logging.getLogger("custom_components.biomatx")

DOMAIN = "biomatx"

CONF_MODULE_COUNT = "module_count"
CONF_SERIAL_WAIT = "serial_wait"
CONF_ALL_OFF_ADDRESS = "all_off_address"
BIOMATX_SIGNAL_UPDATE = "biomatx_signal_update_{}_{}_{}"
