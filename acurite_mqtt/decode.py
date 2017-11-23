#===========================================================================
#
# Decode bridge posting data.
#
#===========================================================================
import logging
import time

LOG = logging.getLogger(__name__)

#------------------------------------------------------------------------
wind_map = {
    '5' : 0,
    '7' : 22.5,
    '3' : 45,
    '1' : 67.5,
    '9' : 90,
    'B' : 112.5,
    'F' : 135,
    'D' : 157.5,
    'C' : 180,
    'E' : 202.5,
    'A' : 225,
    '8' : 247.5,
    '0' : 270,
    '2' : 292.5,
    '6' : 315,
    '4' : 337.5,
    }

#------------------------------------------------------------------------
battery_map = {
    "normal" : 1.0,
    "low" : 0.1,
    }

#------------------------------------------------------------------------
converters = {
    "tempf" : lambda i: {"temp" : float(i)},
    "battery" : lambda i: {"battery" : battery_map.get(i, None)},
    "baromin" : lambda i: {"pressure" : float(i)},
    "humidity" : lambda i: {"humidity" : float(i)},
    "rssi" : lambda i: {"signal" : 0.25 * float(i)},
    "sensor" : lambda i: {"id" : str(i)},
    }

#------------------------------------------------------------------------


def decode(data):
    """Convert posted JSON data to numeric format
    """
    # Not a sensor data post.
    if "sensor" not in data:
        LOG.info("Skipping post with no sensor input")
        return {}

    # Firmware request or download
    elif "firmware" in data:
        LOG.info("Skipping firmware post")
        return {}

    # No time field in the data - record the current time as the time
    # stamp.
    result = {'time' : time.time()}

    # Call the handler function for each element.
    for k, v in data.items():
        func = converters.get(k, None)
        if func:
            result.update(func(v))

    LOG.debug("Decoded result %s", result)
    return result

#===========================================================================
