#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'turtlefirewall-lib.pl';

if( $in{save} ne '' ) {
	getOptionsList();
	foreach my $option (@optionkeys) {
		$fw->AddOption($option, $in{$option} );
	}
	$fw->SaveFirewall();
}

redirect( '' );
