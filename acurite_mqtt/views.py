#===========================================================================
#
# Flask view classes
#
#===========================================================================
import datetime
import logging
import flask.views
from . import decode

LOG = logging.getLogger(__name__)


class Unexpected(flask.views.View):
    """Handle unexpected URL's from the bridge.
    """
    def dispatch_request(self):
        path = flask.request.path
        data = flask.request.args

        # Sometimes we get a path of / w/ data - just ignore it.  Log
        # anything else for later analysis.
        if path or data:
            LOG.error("Unexpected posting: '%s' -> %s", path, data)

        return flask.jsonify(checkversion=224)

#===========================================================================


class DataPost(flask.views.MethodView):
    """Main bridge handler.

    Convert the posted data to json, decode it to useful values, and
    then convert them to MQTT messages.
    """
    def __init__(self, mqtt_client, to_mqtt, version):
        self.client = mqtt_client
        self.to_mqtt = to_mqtt
        self.version = version

    def get(self):
        raw = flask.request.args
        LOG.info("Read: %s", raw)

        try:
            # Convert the raw strings into valid values (floats, units, etc).
            data = decode.decode(raw)

            # Use the MQTT conversion function to get messages.
            # Return is a list of (topic, payload) to publish.
            messages = self.to_mqtt(data)
        except:
            LOG.exception("Error decoding posting %s", raw)
            messages = []

        # Send the messages out.
        for topic, payload in messages:
            try:
                LOG.info("Publish: %s: %s", topic, payload)
                self.client.publish(topic, payload)
            except:
                LOG.exception("Error sending MQTT: %s: %s", topic, payload)

        # Bridge gets the current local time in the response, and a
        # firmware revision number.
        now = datetime.datetime.now()
        ls = "%02d:%02d:%02d" % (now.hour, now.minute, now.second)

        # Standard acurite web site reply - found by watching traffic to
        # the acurite web site.
        return flask.jsonify(
            localtime=ls,
            checkversion=self.version,
            success=1,
            )

#===========================================================================
