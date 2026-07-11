#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParseMime();

&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_configuration'}", $text{'title'}, "" );

if( $in{backup} ) {
	my $backup = $in{backup};
	my $output = &tempname();
	my $confdir = &confdir();

	open TARGZ, "| tar xvz --directory $confdir fw.xml fwuserdefservices.xml >$output 2>&1" or &error( $text{configuration_error1} );
	syswrite(TARGZ, $backup, length($backup));
	close TARGZ;

	open FILE, "<$output";
	while (my $f = <FILE>) { print &ui_alert_box("Restored : ${confdir}/${f}", 'success', undef, undef, ''); }
	close FILE;
	unlink $output;
} else {
	print &ui_alert_box($text{configuration_error_title1}, 'danger', undef, undef, '');
}

&ui_print_footer('configuration.cgi',$text{'index_configuration'});
