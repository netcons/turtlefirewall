#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( $text{'list_ndpirisks_title'}, $text{'title'}, "" );

LoadNdpiRisks( $fw );
showNdpiRisks();
print "<br><br>";

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showNdpiRisks {
	@tds = ( "width=20%", "width=80%" );
	print &ui_columns_start([ "<b>$text{'name'}</b>", "<b>$text{'description'}</b>" ], 100, 0, \@tds);
        my @ndpirisks = $fw->GetNdpiRisksList();
	#foreach my $name (@ndpirisks) {
	foreach $name (sort { $a <=> $b } @ndpirisks) {
		my %ndpirisk = $fw->GetNdpiRisk($name);
	        print &ui_columns_row([ $name, $ndpirisk{'DESCRIPTION'} ], \@tds);
        }
	print &ui_columns_end();
}
