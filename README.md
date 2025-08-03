## Turtle Firewall 2

Turtle Firewall allows you to configure a Linux firewall in a simple and fast way.
It's based on Netfilter iptables. Its operation is easy to understand: you can define the different firewall elements (zones, hosts, networks, geoips, ipsets) and then set the services (port, dpi) you want to control (allow, deny, ratelimit, log) among the different elements or groups of elements.
You can do this by simply editing a XML file or using the web interface [Webmin](http://www.webmin.com/).

Turtle Firewall is an Open Source project written using the perl language and realeased under GPL version 2.0 by Andrea Frigido (Frisoft).

## New Features

- Time, GeoIP and nDPI support.
- Blacklists and Flow Risks.
- Rate Limit support.
- Logging per rule. ( target ACCEPT logs flow, target DROP/REJECT logs action )
- Flow Statistics. ( Netflow nDPI classified historical data to disk )
- Connection Marking. ( for use with tc and iproute )
- Connection Tracking. ( for use with CT helpers )
- NAT Map to Port. ( for port redirection )
- Address Lists and CIDR Networks.
- Item References.

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
xt_set, <br>
xt_tcpmss. <br>
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
