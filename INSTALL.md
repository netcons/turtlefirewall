## Webmin

RHEL.
```
dnf config-manager --set-enabled extras-common
dnf config-manager --set-enabled crb
dnf -y install epel-release

dnf -y install wget
wget https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh -f

dnf -y install webmin
```

Debian.
```
apt-get -y install wget
wget https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh -f

apt-get install webmin --install-recommends
```

## Turtlefirewall Webmin Module

Download source.
```
cd /tmp
wget https://github.com/frisoft/turtlefirewall/archive/master.zip -O turtlefirewall-master.zip
unzip turtlefirewall-master.zip
cd turtlefirewall-master
```

Build source.
```
./build-wbm
```

Install RHEL.
```
dnf -y install perl-XML-Parser perl-Net-CIDR-Lite perl-Text-CSV_XS iptables-nft ipset conntrack-tools rsyslog dos2unix gawk crontabs
/usr/libexec/webmin/install-module.pl /tmp/turtlefirewall-master/build/turtlefirewall-*.wbm.gz
```

Install Debian.
```
apt-get -y install libxml-parser-perl libnet-cidr-lite-perl libtext-csv-xs-perl iptables ipset conntrack rsyslog dos2unix gawk cron-daemon-common
/usr/share/webmin/install-module.pl /tmp/turtlefirewall-master/build/turtlefirewall-*.wbm.gz
```

## Kernel Module Build Requirements

RHEL.
```
if ! (grep -w "10" /etc/redhat-release) > /dev/null 2>&1
 then
  dnf -y install centos-release-hyperscale-experimental
  dnf -y upgrade kernel
  reboot
fi

dnf -y install kernel-devel kernel-headers
dnf -y install kernel-modules-extra
dnf -y install iptables-devel libpcap-devel json-c-devel libgcrypt-devel perl-File-Path
dnf -y install autoconf automake libtool
dnf -y install dkms
systemctl enable dkms --now
```

Debian.
```
apt-get -y install libxtables-dev libpcap-dev libjson-c-dev libgcrypt-dev libmodule-path-perl
apt-get -y install autoconf automake libtool
apt-get -y install dkms
```

## IPT Ratelimit Kernel Module

Download source.
```
VERSION="0.3.3"
cd /usr/src
wget https://github.com/aabc/ipt-ratelimit/archive/master.zip -O ipt-ratelimit-master.zip
unzip ipt-ratelimit-master.zip
mv ipt-ratelimit-master ipt-ratelimit-$VERSION
rm -rf ipt-ratelimit-master.zip
cd ipt-ratelimit-$VERSION
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-ipt-ratelimit.conf ./dkms.conf
sed -i 's/^PACKAGE_VERSION=.*$/PACKAGE_VERSION="$VERSION"/' dkms.conf
dkms add -m ipt-ratelimit -v $VERSION
dkms build -m ipt-ratelimit -v $VERSION
dkms install -m ipt-ratelimit -v $VERSION
```

Install library.
```
make all install
```

## XTables Addons Kernel Module.

Download source.
```
VERSION="3.28"
cd /usr/src
wget https://codeberg.org/jengelh/xtables-addons/releases/download/v${VERSION}/xtables-addons-${VERSION}.tar.xz
tar -xvf xtables-addons-${VERSION}.tar.xz
rm -rf xtables-addons-${VERSION}.tar.xz
cd xtables-addons-$VERSION
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-xtables-addons.conf ./dkms.conf
sed -i 's/^PACKAGE_VERSION=.*$/PACKAGE_VERSION="$VERSION"/' dkms.conf
dkms add -m xtables-addons -v $VERSION
dkms build -m xtables-addons -v $VERSION
dkms install -m xtables-addons -v $VERSION
```

Install library.
```
./configure --without-kbuild --prefix=/usr
make
make install
```

## nDPI Netfilter Kernel Module

Download source.
```
VERSION="4.15.0"
cd /usr/src
wget https://github.com/vel21ripn/nDPI/archive/master.zip -O nDPI-flow_info-4.zip
unzip nDPI-flow_info-4.zip
mv nDPI-flow_info-4 ndpi-netfilter-$VERSION
rm -rf nDPI-flow_info-4.zip
cd ndpi-netfilter-$VERSION
rm -rf windows
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-ndpi-netfilter.conf ./dkms.conf
sed -i 's/^PACKAGE_VERSION=.*$/PACKAGE_VERSION="$VERSION"/' dkms.conf
dkms add -m ndpi-netfilter -v $VERSION
dkms build -m ndpi-netfilter -v $VERSION
dkms install -m ndpi-netfilter -v $VERSION
```

Install library.
```
./autogen.sh
cd ndpi-netfilter
make
make install
```

## XTables Time Kernel Module ( RHEL ONLY )

Download source.
```
VERSION="1.0.0"
cd /usr/src
mkdir xtables-time-$VERSION
cd xtables-time-$VERSION
wget https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/net/netfilter/xt_time.c -O ./xt_time.c
cp /tmp/turtlefirewall-master/dkms/Makefile.xt_time ./Makefile
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-xtables-time.conf ./dkms.conf
sed -i 's/^PACKAGE_VERSION=.*$/PACKAGE_VERSION="$VERSION"/' dkms.conf
dkms add -m xtables-time -v $VERSION
dkms build -m xtables-time -v $VERSION
dkms install -m xtables-time -v $VERSION
```

## Turtlefirewall Setup

Disable default firewall RHEL.
```
systemctl disable firewalld --now
```

Finalise setup via Webmin or command line RHEL.
```
cd /usr/libexec/webmin/turtlefirewall/setup
/usr/bin/env perl setup
cd ..
rm -rf setup*
```

Finalise setup via Webmin or command line Debian.
```
cd /usr/share/webmin/turtlefirewall/setup
/usr/bin/env perl setup
cd ..
rm -rf setup*
```

Download GeoIP database and enable service.
```
/etc/cron.daily/xt_geoip_update
systemctl enable turtlefirewall --now
```