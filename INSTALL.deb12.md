## Debian 12

Activate Repos.
```
cp /usr/share/doc/apt/examples/sources.list /etc/apt/sources.list.d
sed -i "s/^deb cdrom:/#deb cdrom:/" /etc/apt/sources.list
apt-get update
apt-get -y install curl wget dpkg-dev

wget https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh -f

mkdir -p /var/tmp/tfw
cd /var/tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*deb12.deb" \
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

apt-get -y install turtlefirewall
```

Configure */etc/turtlefirewall/fw.xml* or via Webmin and enable Turtle Firewall.
```
systemctl enable turtlefirewall --now
```