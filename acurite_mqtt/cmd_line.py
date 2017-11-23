#===========================================================================
#
# Command line parsing and main entry point.
#
#===========================================================================
import argparse
import logging
import sys
import yaml

from . import mqtt
from .MqttConvert import MqttConvert
from . import server


def parse_args(args):
    """Input is command line arguments w/o arg[0]
    """
    p = argparse.ArgumentParser(prog="acurite-mqtt",
                                description="Acurite->MQTT Server")
    p.add_argument("-l", "--log", metavar="log_File",
                   help="Logging file to use.  If not set, stdout is used")
    p.add_argument("--level", metavar="log_level", type=int, default=30,
                   help="Logging level to use.  10=debug, 20=info,"
                   "30=warn, 40=error, 50=critical")
    p.add_argument("config_file", help="Configuration file path.")

    return p.parse_args(args)


#===========================================================================
def main(mqtt_converter=None):
    args = parse_args(sys.argv[1:])

    # Load the configuration file.
    with open(args.config_file) as f:
        config = yaml.load(f.read())

    # Set up the logging level and output.
    log_args = {
        'level' : args.level,
        'datefmt' : '%Y-%m-%d %H:%M:%S',
        'format' : '%(asctime)s %(levelname)s %(module)s: %(message)s',
        }
    if args.log:
        log_args['filename'] = args.log
    logging.basicConfig(**log_args)

    log = logging.getLogger(__name__)

    # Create the MQTT converter w/ the config inputs.
    if not mqtt_converter:
        mqtt_converter = MqttConvert(config['mqtt'], config['sensors'])

    # Connect to the MQTT broker
    client = mqtt.connect(config['mqtt'])

    # Create the flask application
    app = server.create(client, mqtt_converter, config['firmware_rev'])

    # Start the MQTT as a background thread. This way we can run the web
    # server as the main thread here.
    log.info("Starting MQTT client")
    client.loop_start()

    # Turn off lower level flask and server debugging.
    app.logger.setLevel(max(logging.INFO, args.level))
    wlog = logging.getLogger('werkzeug')
    wlog.setLevel(max(logging.WARNING, args.level))

    # Run the web server
    log.info("Starting web server at port %d", config['http_port'])
    app.run(host="0.0.0.0", port=config['http_port'], debug=False)
