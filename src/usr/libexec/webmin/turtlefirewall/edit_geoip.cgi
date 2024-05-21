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

$new = $in{'new'};

if( $new ) {
	&ui_print_header( "<img src=images/geoip.png hspace=4>$text{'edit_geoip_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/geoip.png hspace=4>$text{'edit_geoip_title_edit'}", $text{'title'}, "" );
}

my $geoip = $in{'geoip'};
my $newgeoip = $in{'newgeoip'};
my %n = $fw->GetGeoip($geoip);
my $ip = $n{'IP'};
my $zone = $n{'ZONE'};
my $description = $n{'DESCRIPTION'};

my @zones = grep(!/FIREWALL/, $fw->GetZoneList());

&LoadCountryCodes($fw);
my $options_countrycode = '';
my @countrycodes = $fw->GetCountryCodesList();
for my $k (@countrycodes) {
	my %country = $fw->GetCountryCode($k);
	$options_countrycode .= qq~<option value="$k"~.($k eq $ip ? ' selected' : '').">$k - $country{DESCRIPTION}</option>";
}

print &ui_subheading($new ? $text{'edit_geoip_title_create'} : $text{'edit_geoip_title_edit'});
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
print &ui_columns_row([ "<img src=images/host.png hspace=4><b>$text{'name'}</b>", $col ], \@tds);
# FIXME
#$col = &ui_select("ip", "$ip", \@countrycodes);
$col = "<select name=ip>$options_countrycode</select>";
# FIXME
print &ui_columns_row([ "<img src=images/countrycode.png hspace=4><b>$text{'countrycode'}</b>", $col ], \@tds);
$col = &ui_select("zone", $zone, \@zones);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'zone'}</b>", $col ], \@tds);
$col = &ui_textbox("description", $description, 60, 0, 60);
print &ui_columns_row([ "<img src=images/info.png hspace=4><b>$text{'description'}</b>", $col ], \@tds);
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
