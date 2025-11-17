#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();

$new = $in{'new'};

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_geoip_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_geoip_title_edit'}";
}
&ui_print_header( "$icons{SHIELD}{IMAGE}$text{'index_icon_items'}", $text{'title'}, "" );

my $geoip = $in{'geoip'};
my $newgeoip = $in{'newgeoip'};
my %n = $fw->GetGeoip($geoip);
my $ip = $n{'IP'};
my $zone = $n{'ZONE'};
my $description = $n{'DESCRIPTION'};

my @zones = grep(!/FIREWALL/, $fw->GetZoneList());

&LoadCountryCodes($fw);
my @items_countrycode = ();
my @countrycodes = $fw->GetCountryCodesList();
for my $k (@countrycodes) {
	my %country = $fw->GetCountryCode($k);
	my @opts = ( "$k", "$k - $country{DESCRIPTION}" );
	push(@items_countrycode, \@opts);
}

print &ui_subheading($heading);
print &ui_form_start("save_geoip.cgi", "post");
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("geoip");
} else {
	$col = &ui_textbox("newgeoip", $in{'geoip'});
	$col .= &ui_hidden("geoip", $in{'geoip'});
}
print &ui_columns_row([ "$icons{GEOIP}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_select("ip", "$ip", \@items_countrycode);
print &ui_columns_row([ "$icons{COUNTRYCODE}{IMAGE}<b>$text{'countrycode'}</b>", $col ], \@tds);
$col = &ui_select("zone", $zone, \@zones);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'zone'}</b>", $col ], \@tds);
$col = &ui_textbox("description", $description, 60, 0, 60);
print &ui_columns_row([ "$icons{DESCRIPTION}{IMAGE}<b>$text{'description'}</b>", $col ], \@tds);
print &ui_columns_end();

print "<table width=100%><tr>";
if( $new ) {
        print '<td>'.&ui_submit( $text{'button_create'}, "new").'</td>';
} else {
        print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
        print '<td style=text-align:right>'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";

print &ui_form_end();

print "<br><br>";
&ui_print_footer('list_items.cgi','items list');
