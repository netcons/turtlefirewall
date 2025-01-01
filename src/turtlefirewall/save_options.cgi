#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';
&ReadParse();

if( $in{save} ne '' ) {
	getOptionsList();
	foreach my $option (@optionkeys) {
		$fw->AddOption($option, $in{$option} );
	}
	$fw->SaveFirewall();
}

&redirect( '' );
