#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';

&ui_print_header( "$icons{SHIELD}{IMAGE}$text{'index_icon_ndpiprotocols'}", $text{'title'}, "" );

&LoadNdpiProtocols($fw);
&showNdpiProtocols();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showNdpiProtocols {
	@tds = ( "width=20%", "width=80%" );
	print &ui_columns_start([ "<b>$text{'name'}</b>", "<b>$text{'category'}</b>" ], 100, 0, \@tds);
        my @ndpiprotocols = $fw->GetNdpiProtocolsList();
	foreach my $name (@ndpiprotocols) {
		my %ndpiprotocol = $fw->GetNdpiProtocol($name);
	        print &ui_columns_row([ "$icons{NDPISERVICE}{IMAGE}$name", "$icons{DESCRIPTION}{IMAGE}$ndpiprotocol{'CATEGORY'}" ], \@tds);
        }
	print &ui_columns_end();
}
