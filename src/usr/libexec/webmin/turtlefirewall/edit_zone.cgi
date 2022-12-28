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

if( $in{'zone'} eq 'FIREWALL' ) {
	redirect('list_items.cgi');
}

$new = $in{'new'};

if( $new ) {
	&ui_print_header( $text{'edit_zone_title_create'}, $text{'title'}, "" );
} else {
	&ui_print_header( $text{'edit_zone_title_edit'}, $text{'title'}, "" );
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
	print "		<input type=\"text\" size=\"13\" maxlength=\"13\" name=\"zone\">";
} else {
	print '		<input type="text" name="newzone" size="13" maxlength="13" value="'.$in{'zone'}.'">';
	print '		<input type="hidden" name="zone" size="13" maxlength="13" value="'.$in{'zone'}.'">';
}
print			'</td></tr>
			<tr>
				<td><b>'.$text{'interface'}.'</b></td>
				<td><input type="text" name="if" value="'.$if.'"> <small><i>'.$text{zone_help}.'</i></small></td>
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
        print '<td>'.&ui_submit( $text{'button_create'}, "new").'</td>';
} else {
        print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
        print '<td align="right">'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";
print "</form>";


print "<br><br>";
&ui_print_footer('list_items.cgi','items list');

