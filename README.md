# Acurite bridge output to MQTT

This application converts Acurite bridge posts to MQTT messages.  It
requires that the bridge posts (HTTP commands) be redirected to this
application.  The application starts a small web server to read those
commands and convert them MQTT messages using a configuration file to
map sensor ID's to locations.

To redirect bridge posts to the server, plug the bridge into a
separate network interface (USB network dongle, or an add on network
card).  Then run something like this.  PORT must match the server post
set in the config file.  eth1 should be the interface the bridge is
plugged in to.

    PORT = 22041
    iptables -t nat -A PREROUTING -m physdev --physdev-in eth1 -p tcp --dport 80 -j REDIRECT --to-port $PORT

Place that command in a script and add it to the end of
/etc/network/interfaces like this:

    pre-up /etc/network/bridge-redirect.sh

The acurite bridge inteface should also be bridged with the regular
interface.  Something like this in /etc/network/interfaces:

    auto br0
    iface br0 inet dhcp
      bridge_ports eth0 eth1
