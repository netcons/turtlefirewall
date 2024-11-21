#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';
&ReadParse();

&ui_print_header( "$icons{COUNTRYCODE}{IMAGE}$text{'list_countrycodes_title'}", $text{'title'}, "" );

&LoadCountryCodes($fw);
&showCountryCodes();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showCountryCodes {
	@tds = ( "width=5%", "width=95%" );
	print &ui_columns_start([ "<b>$text{'name'}</b>", "<b>$text{'description'}</b>" ], 100, 0, \@tds);
        my @countrycodes = $fw->GetCountryCodesList();
	foreach my $name (@countrycodes) {
		my %countrycode = $fw->GetCountryCode($name);
	        print &ui_columns_row([ "$icons{COUNTRYCODE}{IMAGE}$name", "$icons{DESCRIPTION}{IMAGE}$countrycode{'DESCRIPTION'}" ], \@tds);
        }
	print &ui_columns_end();
}
