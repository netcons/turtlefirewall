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

LoadCountryCodes( $fw );

$options_countrycode = '';
my $ip = $in{'ip'};
@countrycodes = $fw->GetCountryCodesList();
for my $k (@countrycodes) {
	my %country = $fw->GetCountryCode($k);
	$options_countrycode .= qq~<option value="$k"~.($k eq $ip ? ' selected' : '').">$k - $country{DESCRIPTION}</option>";
}

&ui_print_header( $text{'list_geoip_title'}, $text{'title'}, "" );

print '<table width="100%"><tr>';
print '<td><b>'.$text{'countrycode'}.'</b></td>';
print '<td>';
print &ui_form_start("geoip.cgi", "post");
print '<select name="ip">'.$options_countrycode.'</select>';
print &ui_submit( $text{'index_searchgeoip'}, "searchgeoip");
print &ui_form_end();
print '</td>';
print '<td align="right">';
print &ui_form_start("geoip.cgi", "post");
print &ui_submit( $text{'index_updategeoip'}, "updategeoip");
print &ui_form_end();
print '</td>';
print '</tr></table>';

if( $in{searchgeoip} ne '' ) {
	print "<br>";
	print "<br><table border width=\"100%\">
		<tr $tb><th>$ip</th></tr>
		<tr $cb><td>";
	print "<pre><tt><small>";
	print qx{/usr/bin/xt_geoip_query -D /usr/share/xt_geoip -4 $ip 2>&1};
	print "</small></tt></pre>";
	print "</td></tr></table>";
}

if( $in{updategeoip} ne '' ) {
	print "<br>";
	print "<table border width=\"100%\">
       		<tr $cb><td>";
	print "<pre><tt>\n";
	print qx{
		cd /var/tmp;
       		/usr/libexec/xtables-addons/xt_geoip_dl;
	       	/usr/libexec/xtables-addons/xt_geoip_build -s;
	       	rm dbip-country-lite.csv 2>&1
		};
	print "</tt></pre>";
	print "</td></tr></table>";
}

print "<br>";

&ui_print_footer('','turtle firewall index');

#sub showCountryCodes {
#	@tds = ( "width=5%", "width=95%" );
#	print &ui_columns_start([ "<b>$text{'name'}</b>", "<b>$text{'description'}</b>" ], 100, 0, \@tds);
#        my @countrycodes = $fw->GetCountryCodesList();
#	foreach my $name (@countrycodes) {
#		my %countrycode = $fw->GetCountryCode($name);
#	        print &ui_columns_row([ $name, $countrycode{'DESCRIPTION'} ], \@tds);
#        }
#	print &ui_columns_end();
#}
