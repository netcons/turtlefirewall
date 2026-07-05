#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

use WebminCore;
&init_config();
&ReadParse();

&ui_print_header( "$icons{ICON}{IMAGE} v ".$fw->Version(), $text{'title'}, "", undef, 1, 1, 0,
		&help_search_link("iptables", "man", "doc"));

# do you need to install startup scripts?
if( -f "./setup/turtlefirewall" ) {

	my $err = 1;
	print "<br>";
	if( chdir("./setup") ) {
		$err = system( '/usr/bin/perl setup' );
		chdir("../");
	}
	if( $err == 0 ) {
		print &ui_alert_box('Congratulations: Turtle Firewall successfully installed', 'success', undef, undef, '');
		system( 'rm -rf setup' );
	} else {
		print &ui_alert_box('Installation error: Turtle Firewall was not successfully installed', 'danger', undef, undef, '');
	}
}

print "<br><br>\n";

&ui_print_footer('index.cgi',$text{'index'});
