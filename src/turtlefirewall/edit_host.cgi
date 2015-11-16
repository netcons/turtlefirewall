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
	&header( $text{'edit_host_title_create'}, '' );
} else {
	&header( $text{'edit_host_title_edit'}, '' );
}

$host = $in{'host'};
%h = $fw->GetHost($host);
$ip = $h{'IP'};
$mac = $h{'MAC'};
$zone = $h{'ZONE'};
$description = $h{'DESCRIPTION'};

$options_zone = '';
@zones = $fw->GetZoneList();
for my $k (@zones) {
	if( $k ne 'FIREWALL' ) {
		$options_zone .= '<option'.($k eq $zone ? ' selected' : '').'>'.$k;
	}
}

print "<br><br>
	<form action=\"save_host.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_host_title_create'} : $text{'edit_host_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
			<td>
				<b>".$text{'name'}."</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"host\">";
} else {
	print '		<input type="text" name="newhost" value="'.$in{'host'}.'">';
	print '		<input type="hidden" name="host" value="'.$in{'host'}.'">';
}
print			qq~</td></tr>
			<tr>
				<td><b>$text{hostaddress}</b></td>
				<td><input type="text" name="ip" value="$ip" size="15"></td>
			</tr>
			<tr>
				<td><b>$text{macaddress}</b> <small><i>($text{optional})</i></small></td>
				<td><input type="text" name="mac" value="$mac" size="17"></td>
			</tr>
			<tr>
				<td><b>$text{'zone'}</b></td>
				<td><select name="zone">$options_zone</select></td>
			</tr>
			<tr>
				<td><b>$text{'description'}</b></td>
				<td><input type="text" size="60" name="description" value="$description"></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>~;

print "<table width=\"100%\"><tr>";
if( $new ) {
	print '<td><input type="submit" name="new" value="'.$text{'button_create'}.'"></td>';
} else {
	print '<td><input type="submit" name="save" value="'.$text{'button_save'}.'"></td>';
	print '<td align="right"><input type="submit" name="delete" value="'.$text{'button_delete'}.'"></td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&footer('list_items.cgi','items list');

