#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

$new = $in{'new'};

if( $new ) {
	&ui_print_header( $text{'edit_geoip_title_create'}, $text{'title'}, "" );
} else {
	&ui_print_header( $text{'edit_geoip_title_edit'}, $text{'title'}, "" );
}

$geoip = $in{'geoip'};
$newgeoip = $in{'newgeoip'};
%n = $fw->GetGeoip($geoip);
$ip = $n{'IP'};
$zone = $n{'ZONE'};
$description = $n{'DESCRIPTION'};

$options_zone = '';
@zones = $fw->GetZoneList();
for my $k (@zones) {
	if( $k ne 'FIREWALL' ) {
		$options_zone .= '<option'.($k eq $zone ? ' selected' : '').'>'.$k;
	}
}

LoadCountryCodes( $fw );
$options_countrycode = '';
@countrycodes = $fw->GetCountryCodesList();
for my $k (@countrycodes) {
	my %country = $fw->GetCountryCode($k);
	$options_countrycode .= qq~<option value="$k"~.($k eq $ip ? ' selected' : '').">$k - $country{DESCRIPTION}";
}

print "<br><br>
	<form action=\"save_geoip.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_geoip_title_create'} : $text{'edit_geoip_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
			<td>
				<b>".$text{'name'}."</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"geoip\">";
} else {
	print '		<input type="text" name="newgeoip" value="'.$in{'geoip'}.'">';
	print '		<input type="hidden" name="geoip" value="'.$in{'geoip'}.'">';
}
print			'</td></tr>
                        <tr>
                                <td><b>'.$text{'countrycode'}.'</b></td>
				<td><select name="ip">'.$options_countrycode.'</select></td>
                        </tr>
			<tr>
				<td><b>'.$text{'zone'}.'</b></td>
				<td><select name="zone">'.$options_zone.'</select></td>
			</tr>
			<tr>
				<td><b>'.$text{'description'}.'</b></td>
				<td><input type="text" size="60" name="description" value="'.$description.'"></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>';

print "<table width=\"100%\"><tr>";
if( $new ) {
        print '<td>'.&ui_submit( $text{'button_create'}, "new").'</td>';
} else {
        print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
        print '<td align="right">'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&ui_print_footer('list_items.cgi','items list');

