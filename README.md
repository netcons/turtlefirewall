## Turtle Firewall 2.1

Turtle Firewall allows you to configure a Linux firewall in a simple and fast way.
It's based on Linux iptables. Its way of working is easy to understand: you can define the different firewall elements (zones, hosts, networks) and then set the services you want to enable among the different elements or groups of elements.
You can do this by simply editing a XML file or using the handy web interface [Webmin](http://www.webmin.com/).

Turtle Firewall is an Open Source project written using the perl language and realeased under GPL version 2.0 by Andrea Frigido (Frisoft).

## New Features

- OS : Systemd support, RPM package, Ensure running via cron.
- OS : Kernel 6.0 compatibility.
- Feature : Added Time, GeoIP and nDPI support.
- Feature : Added Optional Blacklist support.
- Feature : Added NAT Map to Port.
- Feature : Added HostName Set and IP Set items.
- Feature : Added Flow Statistics.
- Feature : Moved Marking to Mangle Rules. ( Connmark : for use with tc )
- Feature : Added Preroute Mangle Rules. ( Connmark Preroute : for use with iproute )
- Feature : Added Preroute Raw Rules. ( Conntrack Helper )
- Logging : Added Logging per rule and Flowinfo logging for target ACCEPT.
- Services : Removed www service. ( duplicate of http service ) 
- Services : Added Google QUIC, Ubiquiti Unifi, Whatsapp, Zoom, Teams, etc.
- Bug : Fixed MAC filtering. ( no ip required )
- Bug : Fixed mangle table flush on firewall stop.
- Bug : Migrated ip_conntrack_max to nf_conntrack_max.
- Bug : Limit zone name max characters.
- Bug : Fixed zone deletion verification.
- Connection Tracking : Replaced "-m state --state" with "-m conntrack --ctstate".
- Connection Tracking : Migrated helpers to CT target.
- Connection Tracking : Enabled connection marking.
- Connection Tracking : Flush conntrack table on firewall stop.
- Connection Tracking : Added conntrack tools.
- Theme : New Webmin support. ( Todo : Translate new features )

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
