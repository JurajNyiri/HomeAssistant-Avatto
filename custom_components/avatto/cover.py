from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from typing import Callable
from .utils import getData, setState
from homeassistant.util import slugify
from .const import DEVICE_IP, DEVICE_ID, DEVICE_KEY, _LOGGER, DEFAULT_DPS, SUPPORT_FLAGS
from homeassistant.components.cover import CoverEntity, ATTR_POSITION


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
):
    try:
        dps = getData(
            entry.data.get(DEVICE_ID),
            entry.data.get(DEVICE_KEY),
            entry.data.get(DEVICE_IP),
        )

        return async_add_entities([AvattoCoverEntity(hass, entry, dps,)])
    except Exception as e:
        _LOGGER.error(e)
    return False


class AvattoCoverEntity(CoverEntity):
    def __init__(self, hass: HomeAssistant, entry: dict, dps):
        super().__init__()
        self.deviceIP = entry.data.get(DEVICE_IP)
        self.deviceID = entry.data.get(DEVICE_ID)
        self.deviceKey = entry.data.get(DEVICE_KEY)
        self._icon = "mdi:blinds"
        if dps is False:
            self.isAvailable = False
            self.dps = DEFAULT_DPS
        else:
            self.isAvailable = True
            self.dps = dps["dps"]

    @property
    def icon(self):
        return self._icon

    def manualUpdate(self):
        newDPS = getData(self.deviceID, self.deviceKey, self.deviceIP)
        if newDPS is False:
            self.isAvailable = False
            _LOGGER.warn(self.deviceIP + " is not available.")
        else:
            self.isAvailable = True
            self.dps = newDPS["dps"]

    def update(self):
        self.manualUpdate()

    @property
    def should_poll(self):
        return True

    @property
    def state(self):
        return self.dps["7"]

    @property
    def supported_features(self):
        return SUPPORT_FLAGS

    @property
    def name(self):
        return slugify(f"avatto_{self.deviceIP}")

    @property
    def device_state_attributes(self):
        attributes = {}

        attributes["countdown"] = self.dps["9"]

        return attributes

    @property
    def current_cover_position(self):
        """Return current position of cover.
        None is unknown, 0 is closed, 100 is fully open.
        """
        return self.dps["3"]

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        return self.dps["3"] == 100

    def close_cover(self, **kwargs):
        setState(self.deviceID, self.deviceKey, self.deviceIP, 100, 2)

    def open_cover(self, **kwargs):
        setState(self.deviceID, self.deviceKey, self.deviceIP, 0, 2)

    def set_cover_position(self, **kwargs):
        setState(self.deviceID, self.deviceKey, self.deviceIP, kwargs[ATTR_POSITION], 2)
