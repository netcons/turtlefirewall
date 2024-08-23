## CentOS/RHEL 10

Activate Repos.
```
dnf config-manager --set-enabled extras-common
dnf config-manager --set-enabled crb
dnf -y install createrepo wget

wget https://download.webmin.com/developers-key.asc -O /etc/pki/rpm-gpg/RPM-GPG-KEY-webmin

echo '[webmin]
name=CentOS Stream $releasever - Webmin
baseurl=https://download.webmin.com/download/newkey/yum/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-webmin
enabled=1'  > /etc/yum.repos.d/webmin.repo

mkdir -p /var/tmp/tfw
cd /var/tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*.el10.*rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
createrepo ./

wget https://raw.githubusercontent.com/netcons/turtlefirewall/master/RPM-GPG-KEY-tfw -O /etc/pki/rpm-gpg/RPM-GPG-KEY-tfw

echo '[tfw]
name=CentOS Stream $releasever - Turtlefirewall
baseurl=file:/var/tmp/tfw/
gpgckeck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-tfw
enabled=1' > /etc/yum.repos.d/tfw.repo
```

Install Turtle Firewall.
```
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

## CentOS/RHEL 9

Activate Repos.
```
dnf config-manager --set-enabled extras-common
dnf config-manager --set-enabled crb
dnf -y install epel-release
dnf -y install centos-release-hyperscale-experimental
dnf -y install createrepo wget

wget https://download.webmin.com/developers-key.asc -O /etc/pki/rpm-gpg/RPM-GPG-KEY-webmin

echo '[webmin]
name=CentOS Stream $releasever - Webmin
baseurl=https://download.webmin.com/download/newkey/yum/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-webmin
enabled=1'  > /etc/yum.repos.d/webmin.repo

mkdir -p /var/tmp/tfw
cd /var/tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*.el9.*rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
createrepo ./

wget https://raw.githubusercontent.com/netcons/turtlefirewall/master/RPM-GPG-KEY-tfw -O /etc/pki/rpm-gpg/RPM-GPG-KEY-tfw

echo '[tfw]
name=CentOS Stream $releasever - Turtlefirewall
baseurl=file:/var/tmp/tfw/
gpgckeck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-tfw
enabled=1' > /etc/yum.repos.d/tfw.repo
```

Install Turtle Firewall.
```
dnf -y upgrade kernel
dnf -y install kernel-devel kernel-headers
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

## CentOS/RHEL 9/10

If dkms does not auto build kernel modules after reboot
```
systemctl is-enabled turtlefirewall > /dev/null
if [ $? = 0 ]
 then
  turtlefirewall
  lsmod | grep xt_geoip > /dev/null
  if [ $? != 0 ]
   then
    ver=`readlink -f /usr/src/xtables-addons-* | cut -d "-" -f3`
    dkms remove -m xtables-addons/${ver} --all
    dkms add -m xtables-addons -v $ver
    dkms build -m xtables-addons -v $ver
    dkms install -m xtables-addons -v $ver
  fi
  lsmod | grep xt_ndpi > /dev/null
  if [ $? != 0 ]
   then
    ver=`readlink -f /usr/src/ndpi-netfilter-* | cut -d "-" -f3`
    dkms remove -m ndpi-netfilter/${ver} --all
    dkms add -m ndpi-netfilter -v $ver
    dkms build -m ndpi-netfilter -v $ver
    dkms install -m ndpi-netfilter -v $ver
  fi
  lsmod | grep xt_ratelimit > /dev/null
  if [ $? != 0 ]
   then
    ver=`readlink -f /usr/src/ipt-ratelimit-* | cut -d "-" -f3`
    dkms remove -m ipt-ratelimit/${ver} --all
    dkms add -m ipt-ratelimit -v $ver
    dkms build -m ipt-ratelimit -v $ver
    dkms install -m ipt-ratelimit -v $ver
  fi
  lsmod | grep xt_time > /dev/null
  if [ $? != 0 ]
   then
    ver=`readlink -f /usr/src/xtables-time-* | cut -d "-" -f3`
    dkms remove -m xtables-time/${ver} --all
    dkms add -m xtables-time -v $ver
    dkms build -m xtables-time -v $ver
    dkms install -m xtables-time -v $ver
  fi
  turtlefirewall
fi
```
