## RHEL 7

Activate Repos.
```
sed -i "s/mirror.centos.org/vault.centos.org/g" /etc/yum.repos.d/*.repo
sed -i "s/^#baseurl=/baseurl=/" /etc/yum.repos.d/*.repo
sed -i "s/^mirrorlist=/#mirrorlist=/" /etc/yum.repos.d/*.repo

yum -y install yum-utils
yum-config-manager --enable repository extras
yum -y install epel-release
yum -y install createrepo wget

yum -y install centos-release-scl
sed -i "s/mirror.centos.org/vault.centos.org/g" /etc/yum.repos.d/CentOS-SCLo-scl*
sed -i "s/^# baseurl=/baseurl=/" /etc/yum.repos.d/CentOS-SCLo-scl*
sed -i "s/^mirrorlist=/#mirrorlist=/" /etc/yum.repos.d/CentOS-SCLo-scl*

wget https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh -f

mkdir -p /var/tmp/tfw
cd /var/tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*.el7.*rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
createrepo ./

echo '[tfw]
name=CentOS-$releasever - Turtlefirewall
baseurl=file:/var/tmp/tfw/
gpgckeck=0
enabled=1' > /etc/yum.repos.d/tfw.repo

sed -i "s/^gpgcheck=.*$/gpgcheck=0/" /etc/yum.conf
```

Install Turtle Firewall.
```
yum -y upgrade kernel
yum -y install kernel-devel kernel-headers
yum -y upgrade iptables iptables-ebtables
yum -y install turtlefirewall
yum -y install devtoolset-9-*
echo "source /opt/rh/devtoolset-9/enable" >> /etc/dkms/framework.conf
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