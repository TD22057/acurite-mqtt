#===========================================================================
#
# MQTT connection
#
#===========================================================================
import paho.mqtt.client


def connect(config):
    client = paho.mqtt.client.Client()

    user = config.get("username", None)
    password = config.get("password", None)
    if user and password:
        client.username_pw_set(user, password)

    client.connect(config['host'], config['port'])
    return client
