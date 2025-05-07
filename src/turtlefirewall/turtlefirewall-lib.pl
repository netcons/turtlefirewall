#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

$|=1;

BEGIN { push(@INC, ".."); };
use WebminCore;
&init_config();

# if XML::Parser is not present
$gotXmlParser = 0;
foreach my $d (@INC) {
	if( -f "$d/XML/Parser.pm" ) {
		$gotXmlParser++;
		break;
	}
}
if( ! $gotXmlParser ) {
	&ui_print_header( undef, $text{'title'}, "" );
	print "<br><br><b>XML::Parser perl module is needed, please install it!</b><br>";
	print '<a href="/cpan/download.cgi?source=3&cpan=XML::Parser&mode=2">install XML::Parser from CPAN</a><br><br>';
	&ui_print_footer('/',$text{'index'});
	exit;
}

# do you need to install startup scripts?
if( -f "./setup/turtlefirewall" ) {
	&ui_print_header( undef, $text{'title'}, "" );
	print "<br>";
	print "<b>This is the first execution of Turtle Firewall, you need to install/update startup scripts.</b>\n";
	print "<br><br>";
	print &ui_form_start("setup.cgi","post");
	print &ui_submit("Install Turtle Firewall Startup scripts","install");
	print &ui_form_end();
	print "<br><b>Notes:</b> ";
	print "Remember to install xt_ndpi, xt_geoip and xt_ratelimit kernel modules.";
	#print "Remember to enable your Linux box to act as a router ";
	#print "(select \"Act as router\"=yes in Hardware->Network->Routing webmin form).";
	#print "<li>Remember to install XML::Parser Perl module</li>";
	print "<br>\n";
	&ui_print_footer('/',$text{'index'});
	exit;
}

my $tfwlib = '/usr/lib/turtlefirewall/TurtleFirewall.pm';
if( ! -f $tfwlib ) {
	&error( 'Turtle Firewall Library not found. Install Turtle Firewall.' );
}

if( -f $config{fw_logfile} ) {
	$SysLogFile = $config{fw_logfile};
} elsif( -f  "/var/log/messages" ) {
	$SysLogFile =  "/var/log/messages";
} elsif( -f  "/var/log/syslog" ) {
	$SysLogFile =  "/var/log/syslog";
}

$FlowLogFile = "/var/log/flowinfo.log";

require $tfwlib;
$fw = new TurtleFirewall();
if( -f $config{fw_file} ) {
	$fw->LoadFirewall( $config{fw_file} );
} else {
	$fw->LoadFirewall( "/etc/turtlefirewall/fw.xml" );
}

sub confdir {
	if( $config{fw_file} =~ /(.*)\// ) {
		return $1;
	} else {
		#return '/tmp';
		return '/etc/turtlefirewall';
	}
}

%flowreports = ( 
	'source' => { LOGIDX => '4', ICOIDX => 'SRC', TXTIDX => 'flowstat_type_source' },
       	'destination' => { LOGIDX => '6', ICOIDX => 'DST', TXTIDX => 'flowstat_type_destination' },
       	'dport' => { LOGIDX => '7', ICOIDX => 'SERVICE', TXTIDX => 'flowstat_type_dport' },
       	'protocol' => { LOGIDX => '16', ICOIDX => 'NDPISERVICE', TXTIDX => 'flowstat_type_protocol' },
       	'hostname' => { LOGIDX => '17', ICOIDX => 'HOSTNAME', TXTIDX => 'flowstat_type_hostname' },
       	'risk' => { LOGIDX => '21', ICOIDX => 'RISK', TXTIDX => 'flowstat_type_risk' }
);

%blacklists = ( 
	'ip_blacklist' => { FILE => '/etc/turtlefirewall/ip_blacklist.dat', TYPE => 'hash:ip', DESCRIPTION => 'IP Address' },
	'domain_blacklist' => { FILE => '/etc/turtlefirewall/domain_blacklist.dat', TYPE => 'ndpi:domain', DESCRIPTION => 'DNS Domain Name' },
	'sha1_blacklist' => { FILE => '/etc/turtlefirewall/sha1_blacklist.dat', TYPE => 'ndpi:sha1', DESCRIPTION => 'SSL Certificate Fingerprint' }
);

%icons = ( 
	'SHIELD' => { IMAGE => '<img src=images/shield.png hspace=4>' },
	'ADDRESSLIST' => { IMAGE => '<img src=images/address.png hspace=4>' },
	'FIREWALL' => { IMAGE => '<img src=images/firewall.png hspace=4>' },
	'ZONE' => { IMAGE => '<img src=images/zone.png hspace=4>' },
	'NET' => { IMAGE => '<img src=images/net.png hspace=4>' },
	'HOST' => { IMAGE => '<img src=images/host.png hspace=4>' },
	'GEOIP' => { IMAGE => '<img src=images/geoip.png hspace=4>' },
	'IPSET' => { IMAGE => '<img src=images/item.png hspace=4>' },
	'GROUP' => { IMAGE => '<img src=images/group.png hspace=4>' },
	'HOSTNAMESET' => { IMAGE => '<img src=images/hostnameset.png hspace=4>' },
	'HOSTNAME' => { IMAGE => '<img src=images/hostname.png hspace=4>' },
	'RISKSET' => { IMAGE => '<img src=images/riskset.png hspace=4>' },
	'RISK' => { IMAGE => '<img src=images/risk.png hspace=4>' },
	'RATELIMIT' => { IMAGE => '<img src=images/ratelimit.png hspace=4>' },
	'RATE' => { IMAGE => '<img src=images/rate.png hspace=4>' },
	'TIME' => { IMAGE => '<img src=images/time.png hspace=4>' },
	'TIMEGROUP' => { IMAGE => '<img src=images/timegroup.png hspace=4>' },
	'TIMESTART' => { IMAGE => '<img src=images/stopwatch.png hspace=4>' },
	'TIMESTOP' => { IMAGE => '<img src=images/stopwatch.png hspace=4>' },
	'RULE' => { IMAGE => '<img src=images/filter.png hspace=4>' },
	'CONNMARKPREROUTE' => { IMAGE => '<img src=images/grey-mark.png hspace=4>' },
	'CONNMARK' => { IMAGE => '<img src=images/grey-mark.png hspace=4>' },
	'CONNTRACKPREROUTE' => { IMAGE => '<img src=images/grey-helper.png hspace=4>' },
	'CONNTRACK' => { IMAGE => '<img src=images/grey-helper.png hspace=4>' },
	'REDIRECT' => { IMAGE => '<img src=images/grey-nat.png hspace=4>' },
	'REDIRECT_A' => { IMAGE => '<img src=images/nat.png hspace=4>' },
	'REDIRECT_NO' => { IMAGE => '<img src=images/red-nat.png hspace=4>' },
	'NAT' => { IMAGE => '<img src=images/grey-nat.png hspace=4>' },
	'NAT_A' => { IMAGE => '<img src=images/nat.png hspace=4>' },
	'NAT_NO' => { IMAGE => '<img src=images/red-nat.png hspace=4>' },
	'MASQUERADE' => { IMAGE => '<img src=images/grey-nat.png hspace=4>' },
	'MASQUERADE_A' => { IMAGE => '<img src=images/nat.png hspace=4>' },
	'MASQUERADE_NO' => { IMAGE => '<img src=images/red-nat.png hspace=4>' },
	'SRC' => { IMAGE => '<img src=images/zone.png hspace=4>' },
	'DST' => { IMAGE => '<img src=images/zone.png hspace=4>' },
	'VIRTUAL' => { IMAGE => '<img src=images/zone.png hspace=4>' },
	'REAL' => { IMAGE => '<img src=images/host.png hspace=4>' },
	'BLACKLIST' => { IMAGE => '<img src=images/blacklist.png hspace=4>' },
	'FILE' => { IMAGE => '<img src=images/file.png hspace=4>' },
	'OPTION' => { IMAGE => '<img src=images/option.png hspace=4>' },
	'DESCRIPTION' => { IMAGE => '<img src=images/info.png hspace=4>' },
	'ADDRESS' => { IMAGE => '<img src=images/address.png hspace=4>' },
	'INTERFACE' => { IMAGE => '<img src=images/interface.png hspace=4>' },
	'CREATE' => { IMAGE => '<img src=images/create.png hspace=4>' },
	'EDIT' => { IMAGE => '<img src=images/edit.png hspace=4>' },
	'NETMASK' => { IMAGE => '<img src=images/mask.png hspace=4>' },
	'COUNTRYCODE' => { IMAGE => '<img src=images/countrycode.png hspace=4>' },
	'ITEM' => { IMAGE => '<img src=images/item.png hspace=4>' },
	'SERVICE' => { IMAGE => '<img src=images/service.png hspace=4>' },
	'NDPISERVICE' => { IMAGE => '<img src=images/grey-ndpi.png hspace=4>' },
	'NDPISERVICE_A' => { IMAGE => '<img src=images/ndpi.png hspace=4>' },
	'LOG' => { IMAGE => '<img src=images/grey-eye.png hspace=4>' },
	'LOG_A' => { IMAGE => '<img src=images/eye.png hspace=4>' },
	'FLOWSTAT' => { IMAGE => '<img src=images/graph.png hspace=4>' },
	'TARGET' => { IMAGE => '<img src=images/target.png hspace=4>' },
	'ACCEPT' => { IMAGE => '<img src=images/grey-yes.png hspace=4>' },
	'ACCEPT_A' => { IMAGE => '<img src=images/yes.png hspace=4>' },
	'DROP' => { IMAGE => '<img src=images/grey-no.png hspace=4>' },
	'DROP_A' => { IMAGE => '<img src=images/no.png hspace=4>' },
	'REJECT' => { IMAGE => '<img src=images/grey-reject.png hspace=4>' },
	'REJECT_A' => { IMAGE => '<img src=images/reject.png hspace=4>' },
	'ID' => { IMAGE => '<img src=images/hash.png hspace=4>' },
	'ACTIVE' => { IMAGE => '<img src=images/active.png hspace=4>' },
	'HELPER' => { IMAGE => '<img src=images/grey-helper.png hspace=4>' },
	'HELPER_A' => { IMAGE => '<img src=images/helper.png hspace=4>' },
	'MARK' => { IMAGE => '<img src=images/grey-mark.png hspace=4>' },
	'MARK_A' => { IMAGE => '<img src=images/mark.png hspace=4>' },
	'TOPORT' => { IMAGE => '<img src=images/toport.png hspace=4>' }
);

sub LoadServices {
	my $firewall = shift;
	my $fwservices_file = $config{'fwservices_file'};
	my $fwuserdefservices_file = $config{'fwuserdefservices_file'};

	if( ! -f $fwservices_file ) {
		$fwservices_file = "/etc/turtlefirewall/fwservices.xml";
	}
	if( ! -f $fwuserdefservices_file ) {
		$fwuserdefservices_file = "/etc/turtlefirewall/fwuserdefservices.xml";
	}
	$firewall->LoadServices( $fwservices_file, $fwuserdefservices_file );
}

sub LoadNdpiProtocols {
	my $firewall = shift;
	my $fwndpiprotocols_file = $config{'fwndpiprotocols_file'};

	if( ! -f $fwndpiprotocols_file ) {
		$fwndpiprotocols_file = "/etc/turtlefirewall/fwndpiprotocols.xml";
	}
	$firewall->LoadNdpiProtocols( $fwndpiprotocols_file );
}

sub LoadNdpiRisks {
	my $firewall = shift;
	my $fwndpirisks_file = $config{'fwndpirisks_file'};

	if( ! -f $fwndpirisks_file ) {
		$fwndpirisks_file = "/etc/turtlefirewall/fwndpirisks.xml";
	}
	$firewall->LoadNdpiRisks( $fwndpirisks_file );
}

sub LoadCountryCodes {
	my $firewall = shift;
	my $fwcountrycodes_file = $config{'fwcountrycodes_file'};

	if( ! -f $fwcountrycodes_file ) {
		$fwcountrycodes_file = "/etc/turtlefirewall/fwcountrycodes.xml";
	}
	$firewall->LoadCountryCodes( $fwcountrycodes_file );
}

# Generates html for service input
sub formService {
	my( $service, $port, $multiple ) = @_;
	my $this = '';

	my @services = split( /,/, $service );

	my $options_service = '';
	&LoadServices($fw);
	for my $k ($fw->GetServicesList()) {
		if( !($k =~ /^(tcp|udp|all)$/) ) {
			my %service = $fw->GetService($k);
			my $selected = 0;
			foreach my $s (@services) {
				if( $k eq $s ) {
					$selected = 1;
					last;
				}
			}
			$options_service .= qq~<option value="$k"~.($selected ? ' SELECTED' : '').">$k - $service{DESCRIPTION}</option>";
		}
	}

	$this .= '<table border="0" cellpadding="0">';
	$this .= '<tr><td><input type="RADIO" name="servicetype" value="1"'.($service eq 'all' ? ' CHECKED' : '')."></td><td>$text{rule_all_services}</td></tr>";

	$this .= '<tr><td><input type="RADIO" name="servicetype" value="2"'.(!($service =~ /^(tcp|udp|all)$/) ? ' CHECKED' : '').'></td>';
		if( $multiple ) {
	$this .= '<td><select name="service2" size="5" MULTIPLE>';
	} else {
		$this .= '<td><select name="service2" size="1">';
	}
	$this .= $options_service;
	$this .= '</select></td></tr>';

	$this .= '<tr><td><input type="RADIO" name="servicetype" value="3"'.($service =~ /^(tcp|udp)$/ ? ' CHECKED' : '').'></td>';
	$this .= '<td><select name="service3" size="1">';
	$this .= '<option'.($service eq 'tcp' ? ' SELECTED' : '').'>tcp</option>';
	$this .= '<option'.($service eq 'udp' ? ' SELECTED' : '').'>udp</option>';
	$this .= '</select>';
	$this .= " $text{rule_port} : <input type=\"TEXT\" name=\"port\" value=\"$port\" size=\"11\" maxlength=\"11\"> <small><i>$text{port_help}</i></small></td></tr></table>";
	return $this;
}

# Parse service inputs and return name of service choosed
sub formServiceParse {
	my ($servicetype, $service2, $service3, $port ) = @_;

	if( $servicetype == 1 ) {
		return ('all', '');
	} elsif( $servicetype == 2 ) {
		# specific service or service list
		$service2 =~ s/\0/,/g;
		return ($service2, '');
	} elsif( $servicetype == 3 ) {
		# generic tcp/udp service
		return ($service3, $port);
	}
	return ('','');
}

# Generates html for ndpiprotocol input
sub formNdpiProtocol {
	my( $ndpiprotocol, $category, $multiple ) = @_;
	my $this = '';

	my @ndpiprotocols = split( /,/, $ndpiprotocol );

	my @categorys = ();

	my $options_ndpiprotocol = '';
	&LoadNdpiProtocols($fw);
	for my $k ($fw->GetNdpiProtocolsList()) {
		if( !($k =~ /^(all)$/) ) {
			my %ndpiprotocol = $fw->GetNdpiProtocol($k);
			my $selected = 0;
			foreach my $n (@ndpiprotocols) {
				if( $k eq $n ) {
					$selected = 1;
					last;
				}
			}
			$options_ndpiprotocol .= qq~<option value="$k"~.($selected ? ' SELECTED' : '').">$k - $ndpiprotocol{CATEGORY}</option>";
			push(@categorys, $ndpiprotocol{CATEGORY});
		}
	}

	# sort
	@categorys = sort(@categorys);
	# unique values
	my $prev = '***none***';
	@categorys = grep($_ ne $prev && (($prev) = $_), @categorys);

	for my $k (@categorys) {
		my $selected = 0;
		if( $k eq $category ) { $selected = 1; }
		$options_category .= qq~<option value="$k"~.($selected ? ' SELECTED' : '').">$k";
	}

	$this .= '<table border="0" cellpadding="0">';
	$this .= '<tr><td><input type="RADIO" name="ndpiprotocoltype" value="1"'.($ndpiprotocol eq 'all' ? ' CHECKED' : '')."></td><td>$text{rule_all_ndpiprotocols}</td></tr>";

	$this .= '<tr><td><input type="RADIO" name="ndpiprotocoltype" value="2"'.(!($ndpiprotocol =~ /^(all)$/) ? ' CHECKED' : '').'></td>';
	if( $multiple ) {
		$this .= '<td><select name="ndpiprotocol2" size="5" MULTIPLE>';
	} else {
		$this .= '<td><select name="ndpiprotocol2" size="1">';
	}
	$this .= $options_ndpiprotocol;
	$this .= '</select></td></tr>';

	$this .= '<tr><td><input type="RADIO" name="ndpiprotocoltype" value="3"'.($category ne '' ? ' CHECKED' : '').'></td>';
	$this .= "<td>$text{category} : ";
	$this .= '<select name="category" size="1">';
	$this .= $options_category;
	$this .= '</select></td></tr></table>';
	return $this;
}

# Parse ndpiprotocol inputs and return name of ndpiprotocol choosen
sub formNdpiProtocolParse {
	my ($ndpiprotocoltype, $ndpiprotocol2, $category ) = @_;

	if( $ndpiprotocoltype == 1 ) {
		return ('all', '');
	} elsif( $ndpiprotocoltype == 2 ) {
		# specific ndpiprotocol or ndpiprotocol list
		$ndpiprotocol2 =~ s/\0/,/g;
		return ($ndpiprotocol2, '');
	} elsif( $ndpiprotocoltype == 3 ) {
		# ndpiprotocol category
		return ('', $category);
	}
	return ('','');
}

sub getOptionsList {
	@optionkeys = ('rp_filter','log_martians',
			'drop_invalid_state', 'drop_invalid_all', 'drop_invalid_none', 'drop_invalid_fin_notack',
			'drop_invalid_syn_fin', 'drop_invalid_syn_rst', 'drop_invalid_fragment',
		       	'drop_ip_blacklist', 'drop_domain_blacklist', 'drop_sha1_blacklist',
			'nf_conntrack_max', 'clamp_mss_to_pmtu', 'log_limit', 'log_limit_burst' );
	%options = ();
	%{$options{rp_filter}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>1 );
	%{$options{log_martians}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>1 );
	%{$options{drop_invalid_state}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_all}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_none}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_fin_notack}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_syn_fin}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_syn_rst}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_fragment}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_ip_blacklist}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_domain_blacklist}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_sha1_blacklist}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{nf_conntrack_max}} = ( 'type'=>'text', 'default'=>262144, 'addunchangeopz'=>0 );
	%{$options{clamp_mss_to_pmtu}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{log_limit}} = ( 'type'=>'text', 'default'=>60, 'addunchangeopz'=>0 );
	%{$options{log_limit_burst}} = ( 'type'=>'text', 'default'=>5, 'addunchangeopz'=>0 );
}

sub roundbytes {
	my $bytes = shift;
	my $n = 0;
	++$n and $bytes /= 1024 until $bytes < 1024;
	return sprintf "%.1f %s", $bytes, ( qw[ B KB MB GB TB ] )[ $n ];
}

1;
