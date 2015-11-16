#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

$|=1;

do '../web-lib.pl';
&init_config();

if( $ENV{REQUEST_METHOD} eq "POST" ) { ReadParseMime(); }
else { ReadParse(); }


# if XML::Parser is not present
$gotXmlParser = 0;
foreach my $d (@INC) {
	if( -f "$d/XML/Parser.pm" ) {
		$gotXmlParser++;
		break;
	}
}
if( ! $gotXmlParser ) {
	&header( $text{'title'}, '', undef, 1 );
	print "<br><br><b>XML::Parser perl module is needed, please install it!</b><br>";
	print '<a href="/cpan/download.cgi?source=3&cpan=XML::Parser&mode=2">install XML::Parser from CPAN</a><br><br>';
	&footer('/',$text{'index'});
	exit;
}


# do you need to install startup scripts?
if( -f "./setup/turtlefirewall" ) {
	&header( $text{'title'}, '', undef, 1 );
	print "<br>";
	print "<b>This is the first execution of Turtle Firewall, you need to install/update startup scripts.</b>\n";
	print "<br><br>";
	print '<form action="setup.cgi"><input type="submit" name="install" value="  Install Turtle Firewall Startup scripts  "></form><br>';
	print "<br><b>Notes:</b> ";
	print "Remember to enable your Linux box to act as a router ";
	print "(select \"Act as router\"=yes in Hardware->Network->Routing webmin form).";
	#print "<li>Remember to install XML::Parser Perl module</li>";
	print "<br>\n";
	&footer('/',$text{'index'});
	exit;
}


my $tfwlib = '/usr/lib/TurtleFirewall.pm';
if( ! -f $tfwlib ) {
	error( 'Turtle Firewall Library not found. Install Turtle Firewall.' );
}

if( -f $config{fw_logfile} ) {
	$SysLogFile = $config{fw_logfile} ;
} else {
	$SysLogFile =  "/var/log/messages";
}

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
		return '/tmp';
		#return '/etc/turtlefirewall';
	}
}

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


###
# Generates html for service input
sub formService {
	my( $service, $port, $multiple ) = @_;

	my @services = split( /,/, $service );

	my $options_service = '';
	LoadServices( $fw );
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
			$options_service .= qq~<option value="$k"~.($selected ? ' SELECTED' : '').">$k - $service{DESCRIPTION}";
		}
	}

	print '<table border="0" cellpadding="0">';
	print '<tr><td><input type="RADIO" name="servicetype" value="1"'.($service eq 'all' ? ' CHECKED' : '')."></td><td>$text{rule_all_services}</td></tr>";

	print '<tr><td><input type="RADIO" name="servicetype" value="2"'.(!($service =~ /^(tcp|udp|all)$/) ? ' CHECKED' : '').'></td>';
	if( $multiple ) {
		print '<td><select name="service2" size="6" MULTIPLE>';
	} else {
		print '<td><select name="service2" size="1">';
	}
	print $options_service;
	print '</select></td></tr>';

	print '<tr><td><input type="RADIO" name="servicetype" value="3"'.($service =~ /^(tcp|udp)$/ ? ' CHECKED' : '').'></td>';
	print '<td><select name="service3" size="1">';
	print '<option'.($service eq 'tcp' ? ' SELECTED' : '').'>tcp</option>';
	print '<option'.($service eq 'udp' ? ' SELECTED' : '').'>udp</option>';
	print '</select>';
	print " $text{rule_port} <input type=\"TEXT\" name=\"port\" value=\"$port\" size=\"5\"></td></tr></table>";

}

###
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

sub getOptionsList {
	@optionkeys = ('rp_filter','log_martians',#'drop_unclean',
			'drop_invalid_state',
			'drop_invalid_all', 'drop_invalid_none', 'drop_invalid_fin_notack',
			'drop_invalid_syn_fin', 'drop_invalid_syn_rst', 
			'drop_invalid_fragment', 'ip_conntrack_max', 'log_limit', 'log_limit_burst' );
	%options = ();
	%{$options{rp_filter}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>1 );
	%{$options{log_martians}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>1 );
	#%{$options{drop_unclean}} = ( 'type'=>'radio', 'default'=>'off', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_state}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_all}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_none}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_fin_notack}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_syn_fin}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_syn_rst}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{drop_invalid_fragment}} = ( 'type'=>'radio', 'default'=>'on', 'addunchangeopz'=>0 );
	%{$options{ip_conntrack_max}} = ( 'type'=>'text', 'default'=>8192, 'addunchangeopz'=>0 );
	%{$options{log_limit}} = ( 'type'=>'text', 'default'=>60, 'addunchangeopz'=>0 );
	%{$options{log_limit_burst}} = ( 'type'=>'text', 'default'=>5, 'addunchangeopz'=>0 );
}

