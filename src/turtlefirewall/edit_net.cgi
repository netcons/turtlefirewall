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
	&header( $text{'edit_net_title_create'}, '' );
} else {
	&header( $text{'edit_net_title_edit'}, '' );
}

$net = $in{'net'};
$newnet = $in{'newnet'};
%n = $fw->GetNet($net);
$ip = $n{'IP'};
$netmask = $n{'NETMASK'};
$zone = $n{'ZONE'};
$description = $n{'DESCRIPTION'};

$options_zone = '';
@zones = $fw->GetZoneList();
for my $k (@zones) {
	if( $k ne 'FIREWALL' ) {
		$options_zone .= '<option'.($k eq $zone ? ' selected' : '').'>'.$k;
	}
}

print "<br><br>
	<form action=\"save_net.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_net_title_create'} : $text{'edit_net_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
			<td>
				<b>".$text{'name'}."</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"net\">";
} else {
	print '		<input type="text" name="newnet" value="'.$in{'net'}.'">';
	print '		<input type="hidden" name="net" value="'.$in{'net'}.'">';
}
print			'</td></tr>
			<tr>
				<td><b>'.$text{'netaddress'}.'</b></td>
				<td><input type="text" name="ip" value="'.$ip.'"></td>
			</tr>
			<tr>
				<td><b>'.$text{'netmask'}.'</b></td>
				<td><input type="text" name="netmask" value="'.$netmask.'"></td>
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
	print '<td><input type="submit" name="new" value="'.$text{button_create}.'"></td>';
} else {
	print '<td><input type="submit" name="save" value="'.$text{button_save}.'"></td>';
	print '<td align="right"><input type="submit" name="delete" value="'.$text{button_delete}.'"></td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&footer('list_items.cgi','items list');

