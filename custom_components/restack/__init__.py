import logging
import asyncio
import aiohttp

from .const import DOMAIN
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

ATTR_NAME = "name"
DEFAULT_NAME = "World"

SERVICE_NAME = "execute"

async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    """Set up is called when Home Assistant is loading our component."""

    _LOGGER.info("Setting up")

    session = async_create_clientsession(hass)
    hass.data[DOMAIN] = {"session": session}

    async def handle_execute(call):
        """Handle the service call."""
        # name = call.data.get(ATTR_NAME, DEFAULT_NAME)
        # hass.states.async_set(f"{DOMAIN}.executed", name)

        _LOGGER.info("Executed call starting")

        hass.states.async_set(f"{DOMAIN}.executed", "calling")

        try:
            response = await asyncio.wait_for(
                session.get(f"https://192.168.5.181:7146/WeatherForecast"),
                timeout=5  # Timeout waarde in seconden
            )
            
            _LOGGER.info("Executed call ended")

            # Check the response status
            if response.status == 200:
                hass.states.async_set(f"{DOMAIN}.executed", "success")
            else:
                hass.states.async_set(f"{DOMAIN}.executed", "failed")
                
        except asyncio.TimeoutError:
            _LOGGER.error("API call timed out")
            hass.states.async_set(f"{DOMAIN}.executed", "timeout")
        except Exception as e:
            _LOGGER.error(f"Error occurred during API call: {str(e)}")
            hass.states.async_set(f"{DOMAIN}.executed", "error")


    _LOGGER.info("Registering services")

    # Register services
    hass.services.async_register(DOMAIN, SERVICE_NAME, handle_execute)

    # Return boolean to indicate that initialization was successful.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup the config entry for my device."""
    # device = MyDevice(entry.data[CONF_HOST])
    # try:
    #     await device.async_setup()
    # except (asyncio.TimeoutError, TimeoutException) as ex:
    #     raise ConfigEntryNotReady(f"Timeout while connecting to {device.ipaddr}") from ex
    return True