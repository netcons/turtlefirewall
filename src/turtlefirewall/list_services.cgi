#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';

&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_services'}", $text{'title'}, "" );

&LoadServices($fw);
&showServices();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showServices {
	@tds = ( "width=20%", "width=80%" );
        print &ui_columns_start([ "<b>$text{'name'}</b>", "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	my @services = $fw->GetServicesList();
	foreach my $name (@services) {
		my %service = $fw->GetService($name);
	        print &ui_columns_row([ "$icons{SERVICE}{IMAGE}$name", "$icons{DESCRIPTION}{IMAGE}$service{'DESCRIPTION'}" ], \@tds);
        }
        print &ui_columns_end();
}
