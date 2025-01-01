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
dnf -y install centos-release-hyperscale-experimental
dnf -y upgrade kernel
reboot

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
cd /usr/src
wget https://github.com/aabc/ipt-ratelimit/archive/master.zip -O ipt-ratelimit-master.zip
unzip ipt-ratelimit-master.zip
mv ipt-ratelimit-master ipt-ratelimit-0.3.3
rm -rf ipt-ratelimit-master.zip
cd ipt-ratelimit-0.3.3
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-ipt-ratelimit.conf ./dkms.conf
dkms add -m ipt-ratelimit -v 0.3.3
dkms build -m ipt-ratelimit -v 0.3.3
dkms install -m ipt-ratelimit -v 0.3.3
```

Install library.
```
make all install
```

## XTables Addons Kernel Module.

Download source.
```
cd /usr/src
wget https://inai.de/files/xtables-addons/xtables-addons-3.27.tar.xz -O xtables-addons-3.27.tar.xz
tar -xvf xtables-addons-3.27.tar.xz
rm -rf xtables-addons-3.27.tar.xz
cd xtables-addons-3.27
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-xtables-addons.conf ./dkms.conf
dkms add -m xtables-addons -v 3.27
dkms build -m xtables-addons -v 3.27
dkms install -m xtables-addons -v 3.27
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
cd /usr/src
wget https://github.com/vel21ripn/nDPI/archive/master.zip -O nDPI-flow_info-4.zip
unzip nDPI-flow_info-4.zip
mv nDPI-flow_info-4 ndpi-netfilter-4.11.0
rm -rf nDPI-flow_info-4.zip
cd ndpi-netfilter-4.11.0
rm -rf windows
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-ndpi-netfilter.conf ./dkms.conf
dkms add -m ndpi-netfilter -v 4.11.0
dkms build -m ndpi-netfilter -v 4.11.0
dkms install -m ndpi-netfilter -v 4.11.0
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
cd /usr/src
mkdir xtables-time-1.0.0
cd xtables-time-1.0.0
wget https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/net/netfilter/xt_time.c -O ./xt_time.c
cp /tmp/turtlefirewall-master/dkms/Makefile.xt_time ./Makefile
```

Install module.
```
cp /tmp/turtlefirewall-master/dkms/dkms-xtables-time.conf ./dkms.conf
dkms add -m xtables-time -v 1.0.0
dkms build -m xtables-time -v 1.0.0
dkms install -m xtables-time -v 1.0.0
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