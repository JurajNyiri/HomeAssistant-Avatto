from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from typing import Callable
from .utils import getData, setState
from homeassistant.util import slugify
from .const import (
    DEVICE_IP,
    DEVICE_ID,
    DEVICE_KEY,
    _LOGGER,
    DEFAULT_DPS,
    SUPPORT_FLAGS,
    MAX_POSITION_WAIT_TIME,
    POSITION_UPDATE_INTERVAL,
    DOMAIN,
    MAX_RETRIES,
)
from homeassistant.components.cover import CoverEntity, ATTR_POSITION
import time


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
):
    try:
        dps = getData(
            entry.data.get(DEVICE_ID),
            entry.data.get(DEVICE_KEY),
            entry.data.get(DEVICE_IP),
        )

        entity = AvattoCoverEntity(hass, entry, dps,)
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}
        hass.data[DOMAIN][entry.entry_id] = {}
        hass.data[DOMAIN][entry.entry_id]["entities"] = [
            entity,
        ]

        return async_add_entities(hass.data[DOMAIN][entry.entry_id]["entities"])
    except Exception as e:
        _LOGGER.error(e)
    return False


class AvattoCoverEntity(CoverEntity):
    def __init__(self, hass: HomeAssistant, entry: dict, dps):
        super().__init__()
        self.deviceIP = entry.data.get(DEVICE_IP)
        self.deviceID = entry.data.get(DEVICE_ID)
        self.deviceKey = entry.data.get(DEVICE_KEY)
        self.entryID = entry.entry_id
        self._state = "idle"
        self._icon = "mdi:blinds"
        if dps is False:
            self.isAvailable = False
            self.dps = DEFAULT_DPS
        else:
            self.isAvailable = True
            self.dps = dps["dps"]
        self.position = int(self.dps["3"])

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
        self.position = int(self.dps["3"])

    def update(self):
        self.manualUpdate()

    @property
    def should_poll(self):
        return True

    @property
    def state(self):
        return self._state

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
        return self.position

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        return int(self.position) == 100

    def close_cover(self, **kwargs):
        return self.setPosition(100)

    def open_cover(self, **kwargs):
        return self.setPosition(0)

    def set_cover_position(self, **kwargs):
        self.setPosition(kwargs[ATTR_POSITION])

    def setPosition(self, newPosition, retries=0):
        oldPosition = self.dps["3"]
        queries = 1
        entity = self.hass.data[DOMAIN][self.entryID]["entities"][0]
        if oldPosition != newPosition:
            if newPosition < oldPosition:
                self._state = "opening"
            else:
                self._state = "closing"
            self.position = int(newPosition)
            # todo: calculate properly
            calculatedPosition = oldPosition
            setState(self.deviceID, self.deviceKey, self.deviceIP, newPosition, 2)
            self.manualUpdate()
            while (
                self.dps["3"] != newPosition
                and queries * POSITION_UPDATE_INTERVAL <= MAX_POSITION_WAIT_TIME
            ):
                if newPosition < oldPosition:
                    if calculatedPosition > newPosition:
                        calculatedPosition = calculatedPosition - 1
                else:
                    if calculatedPosition < newPosition:
                        calculatedPosition = calculatedPosition + 1
                time.sleep(POSITION_UPDATE_INTERVAL / 1000)
                self.manualUpdate()
                self.position = int(calculatedPosition)
                if (queries * POSITION_UPDATE_INTERVAL) % (
                    POSITION_UPDATE_INTERVAL * 4
                ) == 0:
                    entity.async_write_ha_state()
                queries += 1
            self.manualUpdate()
            if int(self.position) != int(newPosition):
                if retries <= MAX_RETRIES:
                    _LOGGER.warn("Retrying setting position to " + str(newPosition))
                    return self.setPosition(newPosition, retries + 1)
                else:
                    _LOGGER.error("Failed to set new position.")
            self._state = "idle"
            entity.async_write_ha_state()
