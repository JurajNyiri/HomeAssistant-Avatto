import logging
from hashlib import md5
from homeassistant.components.cover import (
    SUPPORT_SET_POSITION,
    SUPPORT_OPEN,
    SUPPORT_CLOSE,
)


MAX_GET_DATA_RETRIES = 3

STATE = "state"
ENTITY_ID = "entity_id"
SENSOR = "sensor"
DIFFERENCE = "difference"

DEFAULT_DISCOVER_TIMEOUT = 6.0
DOMAIN = "avatto"
_LOGGER = logging.getLogger(__name__)
UDP_KEY = md5(b"yGAdlopoPVldABfn").digest()

DEVICE_IP = "DEVICE_IP"
DEVICE_KEY = "DEVICE_KEY"
DEVICE_ID = "DEVICE_ID"
SUPPORTED_DEVICES = ["3r8gc33pnqsxfe1g"]
SUPPORT_FLAGS = SUPPORT_SET_POSITION | SUPPORT_OPEN | SUPPORT_CLOSE

ADD_MANUALLY = "Add manually"

SUPPORTED_PRODUCT_KEYS = ["3r8gc33pnqsxfe1g"]
SUPPORTED_VERSIONS = ["3.3"]

DEFAULT_DPS = {
    "1": "stop",
    "2": 100,
    "3": 100,
    "5": False,
    "7": "closing",
    "8": "cancel",
    "9": 0,
    "10": 0,
    "11": 0,
}

MAX_POSITION_WAIT_TIME = 15000
POSITION_UPDATE_INTERVAL = 250
