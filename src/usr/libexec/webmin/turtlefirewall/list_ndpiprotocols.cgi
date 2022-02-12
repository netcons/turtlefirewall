#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( $text{'list_ndpiprotocols_title'}, $text{'title'}, "" );

LoadNdpiProtocols( $fw );
showNdpiProtocols();
print "<br><br>";

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showNdpiProtocols {
	@tds = ( "width=20%", "width=80%" );
	print &ui_columns_start([ "<b>$text{'name'}</b>", "<b>$text{'category'}</b>" ], 100, 0, \@tds);
        my @ndpiprotocols = $fw->GetNdpiProtocolsList();
	foreach my $name (@ndpiprotocols) {
		my %ndpiprotocol = $fw->GetNdpiProtocol($name);
	        print &ui_columns_row([ $name, $ndpiprotocol{'CATEGORY'} ], \@tds);
        }
	print &ui_columns_end();
}
