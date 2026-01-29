## Debian 13

Activate Repos.
```
cp /usr/share/doc/apt/examples/debian.sources /etc/apt/sources.list.d
apt-get update
apt-get -y install curl wget dpkg-dev

wget https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh -f

mkdir -p /var/tmp/tfw
cd /var/tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*.deb" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz

echo "deb [trusted=yes] file:/var/tmp/tfw ./" > /etc/apt/sources.list.d/tfw.list

apt-get update
```

Install Turtle Firewall.
```
apt-get -y upgrade linux-image-amd64 linux-headers-amd64
reboot

apt-get -y install ipt-ratelimit ndpi-netfilter xtables-addons-common
apt-get -y install turtlefirewall
```

Configure */etc/turtlefirewall/fw.xml* or via Webmin and enable Turtle Firewall.
```
systemctl enable turtlefirewall --now
```