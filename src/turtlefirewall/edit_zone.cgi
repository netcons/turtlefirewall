#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

if( $in{'zone'} eq 'FIREWALL' ) {
	redirect('list_items.cgi');
}

$new = $in{'new'};

if( $new ) {
	&header( $text{'edit_zone_title_create'}, '' );
} else {
	&header( $text{'edit_zone_title_edit'}, '' );
}

%z = $fw->GetZone($in{'zone'});
$if = $z{'IF'};
$description = $z{'DESCRIPTION'};

print "<br><br>
	<form action=\"save_zone.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_zone_title_create'} : $text{'edit_zone_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
			<td>
				<b>".$text{'name'}."</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"zone\">";
} else {
	#print '		<tt>'.$in{'zone'}.'</tt><input type="hidden" name="zone" value="'.$in{'zone'}.'">';
	print '		<input type="text" name="newzone" value="'.$in{'zone'}.'">';
	print '		<input type="hidden" name="zone" value="'.$in{'zone'}.'">';
}
print			'</td></tr>
			<tr>
				<td><b>'.$text{'interface'}.'</b></td>
				<td><input type="text" name="if" value="'.$if.'"></td>
			</tr>
			<tr>
				<td><b>'.$text{'description'}.'</b></td>
				<td><input type="text" name="description" size="60" value="'.$description.'"></td>
			</tr></table>
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

