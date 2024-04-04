# hass-biomatx
Home assistant integration for Biomatx

To connect to your biomatx, you need an RS-485 adapter, either to USB or to Ethernet, the serial python library used to communicate supports both: https://pythonhosted.org/pyserial/url_handlers.html.
The serial lines should be connected to the module using a twisted pair connected to the two middle pads of an RJ45 connector
If you number the pads from 1 to 8, the 4 and 5 pads, no matter the way you look at the connector as they are the middle ones.
The easiest is probably to use an ethernet cable, cut one side and use the twisted pair that's connected to the middle pads, most probably the blue/stripped blue one.

I used this serial to ethernet adapter: https://www.waveshare.com/rs232-485-to-eth.htm

Then you can extract the archive into your hass installation directory and restart home assistant.
Go into integrations, add the biomatx integration, configure the device or url according to your adapter.
