#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( "<img src=images/service.png hspace=4>$text{'list_services_title'}", $text{'title'}, "" );

LoadServices( $fw );
showServices();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showServices {
	@tds = ( "width=20%", "width=80%" );
        print &ui_columns_start([ "<b>$text{'name'}</b>", "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	my @services = $fw->GetServicesList();
	foreach my $name (@services) {
		my %service = $fw->GetService($name);
	        print &ui_columns_row([ "<img src=images/service.png hspace=4>$name", "<img src=images/info.png hspace=4>$service{'DESCRIPTION'}" ], \@tds);
        }
        print &ui_columns_end();
	#print '<a href="edit_service.cgi?new=1">create new service</a><br>';
}
