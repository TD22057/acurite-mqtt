#===========================================================================
#
# Main flask web server
#
#===========================================================================
import flask
from . import views


def create(mqtt_client, to_mqtt, firmware_rev):
    app = flask.Flask("acurite-mqtt")

    # Add rules to match an empty post or any other unexpected path.
    # First rule matches / and sets the path variable to empty Second
    # rule matches any other request path.
    unexpected = views.Unexpected.as_view("unexpected")
    app.add_url_rule("/", view_func=unexpected)
    app.add_url_rule("/<path:path>", defaults={'path' : ''},
                     view_func=unexpected)

    # Main handler.  This is the URL that the bridge posts to.
    handler = views.DataPost.as_view("bridge", mqtt_client=mqtt_client,
                                     to_mqtt=to_mqtt, version=firmware_rev)
    app.add_url_rule("/weatherstation/updateweatherstation", view_func=handler)

    return app
