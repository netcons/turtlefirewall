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
$group = $in{'group'};
$newgroup = $in{'newgroup'};

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_group_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_group_title_edit'}";
}
&ui_print_header( "$icons{SHIELD}{IMAGE}$text{'index_icon_items'}", $text{'title'}, "" );

my %g = $fw->GetGroup($group);
my @selected_items = @{$g{ITEMS}};
my $description = $g{'DESCRIPTION'};

my @items = $fw->GetItemsAllowToGroup($group);

print &ui_subheading($heading);
print &ui_form_start("save_group.cgi", "post");
my @tds = ( "width=20% style=vertical-align:top", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("group");
} else {
	$col = &ui_textbox("newgroup", $in{'group'});
	$col .= &ui_hidden("group", $in{'group'});
}
print &ui_columns_row([ "$icons{GROUP}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_select("items", \@selected_items, \@items, 8, 1);
print &ui_columns_row([ "$icons{ITEM}{IMAGE}<b>$text{'groupitems'}</b>", $col ], \@tds);
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
