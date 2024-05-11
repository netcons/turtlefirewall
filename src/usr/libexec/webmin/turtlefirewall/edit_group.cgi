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
$group = $in{'group'};
$newgroup = $in{'newgroup'};

if( $new ) {
	&ui_print_header( "<img src=images/group.png hspace=4>$text{'edit_group_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/group.png hspace=4>$text{'edit_group_title_edit'}", $text{'title'}, "" );
}

my %g = $fw->GetGroup($group);
my @selected_items = @{$g{ITEMS}};
my $description = $g{'DESCRIPTION'};

my $options_group = '';

my @items = ();
push @items, $fw->GetItemsAllowToGroup( $group );
@items = sort { $a <=> $b } @items;
for my $k (@items) {
	my $selected = 0;
	for my $s (@selected_items) {
		if( $k eq $s ) {
			$selected = 1;
			last;
		}
	}
	my $type = lc($fw->GetItemType($k));
	$options_group .= qq~<option value="$k"~.($selected ? ' selected' : '').">$k - $type</option>";
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
				<td><img src=images/group.png hspace=4><b>".$text{'name'}."</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"group\">";
} else {
	print '		<input type="text" name="newgroup" value="'.$group.'">';
	print '		<input type="hidden" name="group" value="'.$group.'">';
}
print			qq~</td></tr>
                   	<tr>
                                <td><img src=images/item.png hspace=4><b>$text{'groupitems'}</b></td>
				<td><select name="items" size="5" multiple>$options_group</select></td>
			</tr>
 			<tr>
				<td><img src=images/info.png hspace=4><b>$text{'description'}</b></td>
				<td valign="top"><input type="text" name="description" size="60" value="$description"></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>~;

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
