## RHEL 10

Activate Repos.
```
dnf config-manager --set-enabled extras-common
dnf config-manager --set-enabled crb
dnf config-manager --save --setopt=optional_metadata_types=filelists
dnf -y install epel-release
dnf -y install centos-release-hyperscale-kernel
dnf -y install createrepo wget

wget https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sh setup-repos.sh -f

mkdir -p /var/tmp/tfw
cd /var/tmp/tfw
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*.el10.*rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
curl -s https://api.github.com/repos/harelba/q/releases/latest \
| grep "browser_download_url.*.rpm" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -
createrepo ./

cd /etc/pki/rpm-gpg
curl -s https://api.github.com/repos/netcons/turtlefirewall/releases \
| grep "browser_download_url.*RPM-GPG-KEY-tfw" \
| cut -d : -f 2,3 \
| tr -d \" \
| wget -qi -

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
reboot

dnf -y install turtlefirewall
systemctl enable dkms --now
```

Disable Firewalld.
```
systemctl disable firewalld --now
```

Configure */etc/turtlefirewall/fw.xml* or via Webmin and enable Turtle Firewall.
```
systemctl enable turtlefirewall --now
```