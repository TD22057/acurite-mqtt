#===========================================================================
#
# MQTT conversion
#
#===========================================================================
# pylint: disable=no-member
import json
import logging

LOG = logging.getLogger(__name__)

class MqttConvert:
    def __init__(self, mqtt_config, sensor_config):
        inputs = ['topic_battery', 'topic_rssi', 'topic_humidity',
                  'topic_temp', 'topic_wind_speed', 'topic_wind_dir',
                  'topic_barometer', 'topic_rain']
        for topic in inputs:
            value = None
            if topic in mqtt_config:
                value = mqtt_config[topic]
                if value.endswith("/"):
                    value = value[:-1]

            setattr(self, topic, value)

        self.sensors = {}
        for d in sensor_config:
            for id, data in d.items():
                id = id.strip()
                self.sensors[id] = data
                LOG.debug("Added sensor '%s' -> %s", id, data)

    #----------------------------------------------------------------------
    def __call__(self, data):
        # List of tuples of (topic, payload)
        messages = []

        sensor_id = data['id']
        sensor_data = self.sensors.get(sensor_id, None)
        if sensor_data:
            location = sensor_data['label']
        else:
            location = "ID %s" % sensor_id

        if self.topic_battery and "battery" in data:
            topic = "%s/%s" % (self.topic_battery, location)
            payload = {
                "time" : data['time'],
                "battery" : data['battery'],
                }
            messages.append((topic, json.dumps(payload)))

        if self.topic_rssi and "signal" in data:
            topic = "%s/%s" % (self.topic_rssi, location)
            payload = {
                "time" : data['time'],
                # Input is 0->1, convert to 0->100
                "rssi" : data['signal'] * 100,
                }
            messages.append((topic, json.dumps(payload)))

        if (self.topic_humidity and "humidity" in data and
                (sensor_data and sensor_data.get('humidity', False))):
            topic = "%s/%s" % (self.topic_humidity, location)
            payload = {
                "time" : data['time'],
                "humidity" : data['humidity']
                }
            messages.append((topic, json.dumps(payload)))

        if self.topic_temp and "temprature" in data:
            topic = "%s/%s" % (self.topic_temp, location)
            payload = {
                "time" : data['time'],
                "temperature" : data['temperature'],
                }
            messages.append((topic, json.dumps(payload)))

        if self.topic_wind_speed and 'windspeed' in data:
            topic = "%s/%s" % (self.topic_wind_speed, location)
            payload = {
                "time" : data['time'],
                "speed" : data['wind_speed'],
                }
            messages.append((topic, json.dumps(payload)))

        if self.topic_wind_dir and "winddir" in data:
            topic = "%s/%s" % (self.topic_wind_dir, location)
            payload = {
                "time" : data['time'],
                "direction" : data['winddir'],
                }
            messages.append((topic, json.dumps(payload)))

        if self.topic_barometer and "pressure" in data:
            topic = "%s/%s" % (self.topic_barometer, location)
            payload = {
                "time" : data['time'],
                "pressure" : data['pressure'],
                }
            messages.append((topic, json.dumps(payload)))

        if self.topic_rain and "rainfall" in data:
            topic = "%s/%s" % (self.topic_rain, location)
            payload = {
                "time" : data['time'],
                "rain" : data['rainfall'],
                }
            messages.append((topic, json.dumps(payload)))

        return messages
