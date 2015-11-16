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
$group = $in{'group'};
$newgroup = $in{'newgroup'};

if( $new ) {
	&header( $text{'edit_group_title_create'}, '' );
} else {
	&header( $text{'edit_group_title_edit'}, '' );
}

@aItems = $fw->GetItemsAllowToGroup( $group );

my %g = $fw->GetGroup($group);
my @groupItems = @{$g{ITEMS}};
my $description = $g{DESCRIPTION};

%aSelectedItems = ();
foreach my $k (@groupItems) {
	$aSelectedItems{$k} = 1;
}

print "<br><br>
	<form action=\"save_group.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_group_title_create'} : $text{'edit_group_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
			<td valign=\"top\">
				<b>".$text{'name'}."</b></td>
			<td valign=\"top\">";
if( $new ) {
	print "		<input type=\"text\" name=\"group\">";
} else {
	print '		<input type="text" name="newgroup" value="'.$group.'">';
	print '		<input type="hidden" name="group" value="'.$group.'">';
}
print			'</td></tr>
			<tr>
				<td valign="top"><b>'.$text{'groupitems'}.'</b></td>
				<td valign="top">
					<table width="100%">';

my $col = 0;
foreach my $i (@aItems) {
	if( $col == 0 ) { print "<tr>"; }
	print "<td width=\"25%\"><nobr><input type=\"checkbox\" name=\"item_$i\" value=\"1\" ";
	print ($aSelectedItems{$i} ? ' checked' : '');
	print "> $i</nobr></td>";
	if( ++$col == 4 ) {
		$col = 0;
		print "</tr>";
	}
}
if( $col < 3 ) { print "</tr>"; }

print					'</table>
				</td>
			</tr>';

print 			'<tr><td valign="top"><b>'.$text{'description'}.'</b></td>';
print			'<td valign="top"><input type="text" name="description" size="60" value="'.$description.'"></td>';
print			'</tr>';

print			'</table>
			</td>
		</tr>
	</table>';

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

