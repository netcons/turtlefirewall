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
$timegroup = $in{'timegroup'};
$newtimegroup = $in{'newtimegroup'};

if( $new ) {
	&ui_print_header( "<img src=images/timegroup.png hspace=4>$text{'edit_timegroup_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/timegroup.png hspace=4>$text{'edit_timegroup_title_edit'}", $text{'title'}, "" );
}

@aItems = $fw->GetItemsAllowToTimeGroup( $timegroup );

my %g = $fw->GetTimeGroup($timegroup);
my @timegroupItems = @{$g{ITEMS}};
my $description = $g{DESCRIPTION};

%aSelectedItems = ();
foreach my $k (@timegroupItems) {
	$aSelectedItems{$k} = 1;
}

print "<br><br>
	<form action=\"save_timegroup.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_timegroup_title_create'} : $text{'edit_timegroup_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
			<td valign=\"top\">
				<b>".$text{'name'}."</b></td>
			<td valign=\"top\">";
if( $new ) {
	print "		<input type=\"text\" name=\"timegroup\">";
} else {
	print '		<input type="text" name="newtimegroup" value="'.$timegroup.'">';
	print '		<input type="hidden" name="timegroup" value="'.$timegroup.'">';
}
print			'</td></tr>
			<tr>
				<td valign="top"><b>'.$text{'timegroupitems'}.'</b></td>
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
        print '<td>'.&ui_submit( $text{'button_create'}, "new").'</td>';
} else {
        print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
        print '<td align="right">'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&ui_print_footer('list_items.cgi','items list');

