## RHEL 8

Activate Repos.
```
sed -i "s/mirror.centos.org/vault.centos.org/g" /etc/yum.repos.d/*.repo
sed -i "s/^#baseurl=/baseurl=/" /etc/yum.repos.d/*.repo
sed -i "s/^mirrorlist=/#mirrorlist=/" /etc/yum.repos.d/*.repo

dnf config-manager --set-enabled extras-common
dnf config-manager --set-enabled powertools
dnf -y install epel-release
dnf -y install createrepo wget

dnf -y install centos-release-hyperscale-experimental
sed -i "s/mirror.centos.org/vault.centos.org/g" /etc/yum.repos.d/CentOS-Stream-Hyperscale*
sed -i "s/^#baseurl=/baseurl=/" /etc/yum.repos.d/CentOS-Stream-Hyperscale*
sed -i "s/^mirrorlist=/#mirrorlist=/" /etc/yum.repos.d/CentOS-Stream-Hyperscale*

wget https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh -f

mkdir -p /var/tmp/tfw
cd /var/tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*.el8.*rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
createrepo ./

echo '[tfw]
name=CentOS Stream $releasever - Turtlefirewall
baseurl=file:/var/tmp/tfw/
gpgckeck=0
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