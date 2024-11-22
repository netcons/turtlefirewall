## Turtle Firewall 2

Turtle Firewall allows you to configure a Linux firewall in a simple and fast way.
It's based on Netfilter iptables. Its operation is easy to understand: you can define the different firewall elements (zones, hosts, networks, geoip, ipset) and then set the services (port, dpi) you want to control (allow, deny, ratelimit, log) among the different elements or groups of elements.
You can do this by simply editing a XML file or using the web interface [Webmin](http://www.webmin.com/).

Turtle Firewall is an Open Source project written using the perl language and realeased under GPL version 2.0 by Andrea Frigido (Frisoft).

## New Features

- Time.
- Geo Location.
- Deep Packet Inspection.
- Risk Detection.
- Rate Limiting.
- Blacklists.
- NAT Map to Port.
- Logging per rule.
- Flow Info logging.
- Flow Statistics.
- Connection Marking.
- Connection Tracking.
- Item References.
- CIDR Networks.
- IP Sets.

## Requirements

- expat library installed.
- XML::Parser perl module installed.
- Webmin installed. ( https://github.com/webmin/webmin )
- iptables command in PATH.
- Standard Netfilter kernel modules : <br>
nf_tables, <br>
nf_conntrack, <br>
xt_connmark, <br>
xt_time, <br>
xt_set. <br>
- Extra Netfilter kernel modules : <br>
xt_ndpi, ( https://github.com/vel21ripn/nDPI ) <br>
xt_geoip, ( https://codeberg.org/jengelh/xtables-addons ) <br>
xt_ratelimit. ( https://github.com/aabc/ipt-ratelimit ) <br>

## Contributors

Big thanks to our contributors!

- John Cameron ([netcons](https://github.com/netcons))
- Giampaolo Tomassoni
- Mark Francis
- Alain Terriault
- Jimmy Collins
- Joe MacDonald
- Chris Carter
- Patrik
- Fredrik Tuomas
- Karl Lovink
- Frank Förster
