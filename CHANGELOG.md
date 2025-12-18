# ChangeLog

## v.2.7 (11-12-2025)
- Feature : nDPI 5.1 support.
- Bug: Fix variable declarations.
- Bug: Add invalid service check.
- Todo : Translate new features.
- Todo : Fix backup.cgi restore upload.

## v.2.6 (30-04-2025)
- Feature : nDPI 4.15 support.
- Feature : Remove JA3 logging.
- Feature : Remove JA3 Blacklist.
- Feature : Remove TLS Version logging, already included in JA4.
- Feature : Migrate Flow Statistics query backend to q-text-as-data
  and allow multiple log selection.
- Feature : Add static Blacklist include.
- Bug : Fixed translation of HTML character entities.
- Bug : Fixed Flow Statistics flow time reported incorrectly.
- Bug : Removed default variable reference in log views.
- Bug : Standardize library include and table syntax.
- Bug : Fixed missing sort in item selection.
- Bug : Fixed custom config file definition.
- Bug : Fixed connection marking.
- OS : Remove unused iptables_restore_emu.
- OS : Remove depreciated dkms feature: CLEAN
- Theme : Webmin 2.600 support.
- Theme : Update lib to use ui standard.

## v.2.5 (01-01-2025)
- Services : Make user defined services permanent.
- Services : Removed depreciated kazaa and edonkey services.
- Feature : nDPI 4.13 support.
- Feature : Add clamp_mss_to_pmtu option.
- Feature : Add nDPI ACCEPT support for Hostnames.

## v.2.4 (22-08-2024)
- OS : Old fw.xml format fixes in fixconfig.sh.
- OS : Restore setup.cgi for WBM install.
- OS : Support for Debian 12 syslog date format.
- OS : Standardize shebang.
- Bug : Fixed ApplyRule risk variable not initialised.
- Bug : Fixed GeoIP include for Masquerade and Redirect.
- Bug : Include reserved name check on item rename.
- Bug : Fixed rule highlighting on move.
- Bug : Fixed rule tcp/udp ALL ports display.
- Services : Removed depreciated smtps TCP port 465 service.
- Services : Added DNS over TLS TCP port 853 service.
- Feature : nDPI 4.11 support.
- Feature : Add ipset support.
- Feature : Add prefix support for net items.
- Feature : Add item reference lookup support.
- Feature : Make rule order configurable.

## v.2.3 (18-02-2024)
- Bug : Code cleanup.
- Bug : Fixed --mac-source masquerade.
- Bug : Removed depreciated HTML \<tt\>, \<strike\>, \<font\>, \<align\> and \<valign\> tags.
- Bug : Limit Blacklist sizes.
- Bug : Remove Domain Blacklist wildcard match.
- Bug : Fixed zone name item verification.
- Bug : Fixed Rate Limit apply when used in multiple rules.
- Feature : Rework action log format.
- Feature : Extend nDPI support.
- Logging : Replaced JA3 server with JA4 client.
- Theme : Rework group item selection.
- Theme : Split Port and nDPI service column in rule views.
- Theme : Update edit forms to use ui standard.
- Theme : Standardize Webmin images.

## v.2.2 (03-06-2023)
- Bug : Code cleanup.
- Bug : Fixed rename and delete of multi select items used in rules.
- Bug : Fixed port or port range verification in rules.
- Bug : Fixed service display wrap in rules.
- Feature : Added Flow Risk support.
- Feature : Added Optional Domain, JA3 and SHA1 Blacklist support.
- Feature : Added Rate Limit support.
- Feature : Added "dport" Flow Statistics option.
- Feature : Removed Blacklist Flow Reports. 
- Feature : Improve Blacklist view.

## v.2.1 (09-10-2022)
- OS : Kernel 6 compatibility.
- Feature : Removed pptp, sip, h323 and tftp kernel module options.
- Feature : Added Preroute Raw Rules. ( Conntrack Preroute : for use with CT helpers )
- Feature : Added Raw Rules. ( Conntrack : for use with CT helpers )
- Connection Tracking : Migrated helpers to CT target.

## v.2.0 (23-04-2020)
- OS : Systemd support, RPM package, Ensure running via cron.
- Feature : Added Time, GeoIP and nDPI support.
- Feature : Added Optional IP Blacklist.
- Feature : Added NAT Map to Port.
- Feature : Added HostName Set and IP Set items.
- Feature : Added pptp, sip, h323 and tftp kernel module options.
- Feature : Added Flow Statistics.
- Feature : Moved Marking to Mangle Rules. ( Connmark : for use with tc )
- Feature : Added Preroute Mangle Rules. ( Connmark Preroute : for use with iproute )
- Logging : Added Logging per rule and Flowinfo logging for target ACCEPT.
- Services : Removed www service. ( duplicate of http service ) 
- Services : Added Google QUIC, Ubiquiti Unifi, Whatsapp, Zoom, Teams, etc.
- Bug : Fixed MAC filtering. ( no ip required )
- Bug : Fixed Mangle table flush on firewall stop.
- Bug : Migrated ip_conntrack_max to nf_conntrack_max.
- Bug : Limit zone name max characters.
- Bug : Fixed zone deletion verification.
- Connection Tracking : Replaced "-m state --state" with "-m conntrack --ctstate".
- Connection Tracking : Enabled automatic helpers. ( Todo : migrate to CT target )
- Connection Tracking : Enabled connection marking.
- Connection Tracking : Flush conntrack table on firewall stop.
- Connection Tracking : Added conntrack tools.
- Theme : New Webmin support.

## v.1.38 (20-05-2011)
- Debian 6.0 compatibility (chocolateboy).

## v.1.37 (02-02-2006)
- New service definitions were added:
  igmp (Internet Group Management Protocol).
  bpalogin (BPALogin).
  Thanks to Rene Cunningham for this two services.
  openvpn (OpenVPN protocolo, www.openvpn.net).
- Bugs were fixed.

## v.1.36 (11-01-2006)
- Add multisources and multidestinations in firewall rules.
- Add service attribute in filter xml tag of services definition files.
- Eliminate drop_unclean option, doesn't work with kernel 2.6.x
- Bugfix.

## v.1.34 (31-11-2005)
- Add mangle mark rule attribute for QoS (iproute2).
- Bugfix on turtlefirewall stop procedure (signaled by Ulf Seltmann).

## v.1.33 (??-??-2005)
- Add source and destination option to the NAT rules.
- Bugfix on rules with target REJECT (from v.1.32).

## v.1.32 (17-02-2005)
- Use iptables-restore command to speed up firewall start up.

## v.1.31 (30-11-2004)
- Change rules display in turtlefirewall startup. 
- Fix bugs.

## v.1.30 (21-11-2004)
- Add * option in source and destination field of a firewall rule: all zones except FIREWALL.

## v.1.29 (19-11-2004)
- Set icmp_echo_ignore_all flag to 0. Turtle Firewall use iptables 
  rules for drop or allow icmp echo packets. This fix a bug in tfw ping.
- Disable tcp_ecn flag.
- In masquerading configuration now you can specify source,destinatio,service,
  port and action (masquerade or not masquerade).

## v.1.28 (15-07-2004)
- Add port 445 to netbios service.
- Add jabber and jabber-s2s (server to server) services.
- Add lpr Line Printer Protocol.
- Add rdp - Windows Remote Desktop Protocol.
- Fix bugs.

## v.1.27 (14-05-2003)
- Small Bug-fix.

## v.1.26 (07-05-2003)
- Fix "de" language file (Frank Förster).
- NAT Improved, now you can change rules order.
- NAT rules bugfix.
- Configuration backup download bugfix.

## v.1.25 (02-04-2003)
- Fix bugs.

## v.1.24 (31-03-2003)
- Change Turtle Firewall stop process, ping will be reenabled.
- Add AIM/ICQ and Soulseek std services (Frank Förster).
- Add Oracle, VNC, VNC-http services.
- Add rip, syslog, icecast, icp, irc (Karl Lovink).
- Local Redirection Improved.
- Now you can rename all firewall items.
- More options.

## v.1.23 (18-02-2003)
- Add proxy, ssh21, dhcp, snmptrap, socks and eDonkey services (Karl Lovink).
- Fix a bug into log viewer (Fredrik Tuomas).
- Add Configuration Backup/Restore.

## v.1.22 (02-02-2003)
- Firewall and NAT rules with multiple services.
- Change LOG prefix from "TFW DROP" to "TFW".
- Add --start, --stop and --status options to turtlefirewall main script.
- Add stop button in the webmin turtlefirewall index page.
- Translate error messages (english and italian).
- Add icmp_all service for all messages (request+reply).
- Add all icmp messages in the special service "all".
   
## v.1.21 (16-01-2003)
- Fix a bug in Redirection.

## v.1.20 (15-01-2003)
- Add optional MAC address field in host edit form.
- Add target field (ACCEPT/DROP/REJECT) in rule edit form.
- Fix bug in Log prefix string, it must be up to 29 chars length.
- Add x11: X Window System service.
- Use numerical notation for ports in fwservices.xml.
- Add Active flag to NAT, Masquerade and Redirect rules.
   
## v.1.19 (26-11-2002)
- Fix bug in Zone deletion.
- Fix a bug using aliased interfaces (signaled by Torsten)
- Add German translation (Jimmy Collins)
- Add mysql and kazaa services (Jimmy Collins)
- Add pptp (vpn) and rdp services (Joe MacDonald)
- Add PC-Anyware service (Chris Carter)
- Change setup script for Slackware Linux distribution (A.Frigido, Patrik)

## v.1.18 (13-11-2002)
- Add Firewall Configuration Options.
- Now you can change firewall rules order (more readable).
- Add fwuserdefservices.xml file for userdefined services. With this file you can write your own
  services filter without changing official fwservices.xml file.
  The structure of this new file is identical of fwservices.xml file structure.
  If you write a service with a name used by fwservices.xml, this new service definition overwrite
  the original service definition so, if you want, you can rewrite all services.
  IMPORTANT: I invite all to send me your userdefined service filter definitions, so I can add them into
  the predefined services list (fwservices.xml) for all Turtle Firewall users.
  
## v.1.17 (16-10-2002)
- Fix bug with "--log-level info" iptables option.
- Enhanced log report.
- Enhanced interface.
- Add afp-over-tcp service: AFP (Apple Filing Protocol) over TCP.
  (Alain Terriault)
- Add nfs (experimental)

## v.1.16 (26-09-2002)
- Change webmin category from System to Networking.
- Fix a bug on tcp/udp Local Redirection (Soep).

## v.1.15 (13-09-2002)
- Fix "DROP INVALID unclean" bug.

## v.1.14 (10-09-2002)
- The configurable options contains now the option to select the logfile (Karl Lovink)
- The dutch language has been added (Karl Lovink).

## v.1.13 (03-09-2002)
- Add NAT from a zone interface to a real host (etc. modem interface ip to my pc host).
- Add Redirect module (For Transparent Proxy).
- Fix security hole with INVALID packets filter code by Mark Francis.
- Enhanced Log.
- Add firewall rules for IPsec VPN service.
- Add firewall rules for Webmin service.

## v.1.12 (09-07-2002)
- Fix bug in XML::Parser module checking.

## v.1.11 (08-07-2002)
- Setup procedure into webmin module, now Turtle Firewall installation is very easy.
- Removed chkconfig command for setup, it isn't availabe in all GNU/Linux distributions.
- Fix bug in "Create Nat" web interface.
- Other minor changes.

## v.1.10 (26-06-2002)
- Add description field for rules and items.
- Add experimental H.323 service.
- Fix bugs.

## v.1.00 (20-06-2002)
- Change SystemV service start/stop order from 00/99 to 08/92.
- Change TurtleFirewall package file name.
- Check if XML::Parser perl module is installed.
- Add Telnet service.

## v.0.99 (14-06-2002)
- Fix turtlefirewall privileges bug.
- Use iptables from PATH (iptables directory need to be in PATH env. var.)
- PreLoad modules for ftp connections and NAT.
- Add CVS, NNTP services.
 
## v.0.98 (23-05-2002)
- Do you need port-based natting? Here it is... (Giampaolo Tomassoni)
- Fixed the I-Wanna-Reply-To-Pings-But-It-Doesn't bug: when
  the fw accepts pings on a <somewere> => FIREWALL base,
  don't turn the /proc/sys/net/ipv4/icmp_echo_ignore_all
  kernel flag on... (Giampaolo Tomassoni)
- Applied few ahestetic make-ups (Giampaolo Tomassoni)

## v.0.97 (17-05-2002)
- Add franch webmin language file.
- Fix bugs.

## v.0.96 (17-04-2002)
- Add webmin module languages files for English and Italian.
- Fix Masquerade and NAT bug.

## v.0.95 (02-04-2002)
- Aggiunto il file setup al tarball.

## v.0.94 (22-03-2002)
- Aggiunto supporto dell'attributo ACTIVE delle rule.

## v.0.93 (19-03-2002)
- Aggiunto l'uso del modulo turtlefirewall.pm (/usr/lib)

## v.0.92 (10-01-2002)
- Inserite le regole di accesso da/verso interfaccia lo
  che precedentemente impedivano l'accesso a se stesso.
- Impostati i diritti sul file sh generato per l'esecuzione.
- Corretta la definizione delle lan nei file di configurazione
  di esempio (samples).

## v.0.91 (05-12-2001)
- Modificato il nome da fwconf in Turtle Firewall (turtlefw)
