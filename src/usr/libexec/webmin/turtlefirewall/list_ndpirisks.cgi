#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( "<img src=images/risk.png hspace=4>$text{'list_ndpirisks_title'}", $text{'title'}, "" );

LoadNdpiRisks( $fw );
showNdpiRisks();
print "<br><br>";

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showNdpiRisks {
	@tds = ( "width=5%", "width=95%" );
	print &ui_columns_start([ "<b>$text{'id'}</b>", "<b>$text{'description'}</b>" ], 100, 0, \@tds);
        my @ndpirisks = $fw->GetNdpiRisksList();
	foreach $id (sort { $a <=> $b } @ndpirisks) {
		my %ndpirisk = $fw->GetNdpiRisk($id);
	        print &ui_columns_row([ "<img src=images/risk.png hspace=4>$id", $ndpirisk{'DESCRIPTION'} ], \@tds);
        }
	print &ui_columns_end();
}
