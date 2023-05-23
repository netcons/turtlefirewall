## Turtle Firewall 2.2

Turtle Firewall allows you to configure a Linux firewall in a simple and fast way.
It's based on Linux iptables. Its way of working is easy to understand: you can define the different firewall elements (zones, hosts, networks) and then set the services you want to enable among the different elements or groups of elements.
You can do this by simply editing a XML file or using the handy web interface [Webmin](http://www.webmin.com/).

Turtle Firewall is an Open Source project written using the perl language and realeased under GPL version 2.0 by Andrea Frigido (Frisoft).

## New Features

- Time, GeoIP and nDPI support.
- Optional IP and Domain Blacklist support.
- NAT Map to Port.
- Flow Statistics.
- Logging per rule for Allow and Deny.
- Connection marking rules.
- Connection tracking rules.

## Requirements

- expat library installed.
- XML::Parser perl module installed.
- Webmin installed. ( https://www.webmin.com )
- iptables command in PATH.
- Standard Netfilter kernel modules : <br>
nf_tables, <br>
nf_conntrack, <br>
xt_connmark, <br>
xt_connlabel, <br>
xt_time. <br>
- Extra Netfilter kernel modules : <br>
xt_ndpi, ( https://github.com/vel21ripn/nDPI ) <br>
xt_geoip, ( https://inai.de/projects/xtables-addons ) <br>

## Install CentOS/RHEL 9

Activate Repos.
```
dnf config-manager --set-enabled extras-common
dnf -y install epel-release

echo "[Webmin]
name=Webmin Distribution Neutral
#baseurl=https://download.webmin.com/download/yum
mirrorlist=https://download.webmin.com/download/yum/mirrorlist
enabled=1
gpgkey=https://download.webmin.com/jcameron-key.asc
gpgcheck=1" > /etc/yum.repos.d/webmin.repo

echo "[TFW]
name=Turtle Firewall
baseurl=file:/tmp/tfw/
enabled=1
gpgckeck=0" > /etc/yum.repos.d/tfw.repo

dnf -y install createrepo
mkdir -p /tmp/tfw
cd /tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases/latest \
| grep "browser_download_url.*rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
createrepo ./
sed -i "s/^gpgcheck=.*$/gpgcheck=0/" /etc/yum.conf
 ```

Install Turtle Firewall.
```
dnf -y upgrade kernel kernel-devel kernel-headers
dnf -y install turtlefirewall
systemctl enable dkms --now
reboot
```

Disable Firewalld.
```
systemctl disable firewalld --now
```

Configure */etc/turtlefirewall/fw.xml* or via Webmin and enable Turtle Firewall.
```
systemctl enable turtlefirewall --now
```
