#!/usr/bin/env bash
#
# Add version 2 settings and remove depreciated version 1 settings
#

grep 'name="drop_ip_blacklist"' /etc/turtlefirewall/fw.xml > /dev/null
if [ $? != 0 ]
 then
  sed -i '/^<\/options>$/ i\<option value="on" name="drop_ip_blacklist"\/>' /etc/turtlefirewall/fw.xml
fi

grep 'name="drop_domain_blacklist"' /etc/turtlefirewall/fw.xml > /dev/null
if [ $? != 0 ]
 then
  sed -i '/^<\/options>$/ i\<option value="on" name="drop_domain_blacklist"\/>' /etc/turtlefirewall/fw.xml
fi

grep 'name="drop_ja3_blacklist"' /etc/turtlefirewall/fw.xml > /dev/null
if [ $? != 0 ]
 then
  sed -i '/^<\/options>$/ i\<option value="on" name="drop_ja3_blacklist"\/>' /etc/turtlefirewall/fw.xml
fi

grep 'name="drop_sha1_blacklist"' /etc/turtlefirewall/fw.xml > /dev/null
if [ $? != 0 ]
 then
  sed -i '/^<\/options>$/ i\<option value="on" name="drop_sha1_blacklist"\/>' /etc/turtlefirewall/fw.xml
fi

grep 'name="nf_conntrack_max"' /etc/turtlefirewall/fw.xml > /dev/null
if [ $? != 0 ]
 then
  sed -i '/^<\/options>$/ i\<option name="nf_conntrack_max" value="262144"\/>' /etc/turtlefirewall/fw.xml
fi

sed -i '/name="ip_conntrack_max"/d' /etc/turtlefirewall/fw.xml
sed -i '/name="drop_unclean"/d' /etc/turtlefirewall/fw.xml
