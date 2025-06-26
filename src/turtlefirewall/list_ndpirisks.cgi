#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';

&ui_print_header( "$icons{RISK}{IMAGE}$text{'list_ndpirisks_title'}", $text{'title'}, "" );

&LoadNdpiRisks($fw);
&showNdpiRisks();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showNdpiRisks {
	@tds = ( "width=5%", "width=95%" );
	print &ui_columns_start([ "<b>$text{'id'}</b>", "<b>$text{'description'}</b>" ], 100, 0, \@tds);
        my @ndpirisks = $fw->GetNdpiRisksList();
	foreach $id (sort { $a <=> $b } @ndpirisks) {
		my %ndpirisk = $fw->GetNdpiRisk($id);
	        print &ui_columns_row([ "$icons{RISK}{IMAGE}$id", "$icons{DESCRIPTION}{IMAGE}$ndpirisk{'DESCRIPTION'}" ], \@tds);
        }
	print &ui_columns_end();
}
