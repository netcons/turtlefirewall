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
$timegroup = $in{'timegroup'};
$newtimegroup = $in{'newtimegroup'};

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_timegroup_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_timegroup_title_edit'}";
}
&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_items'}", $text{'title'}, "" );

my %g = $fw->GetTimeGroup($timegroup);
my @selected_items = @{$g{ITEMS}};
my $description = $g{DESCRIPTION};

my @items = $fw->GetItemsAllowToTimeGroup($timegroup);

print &ui_subheading($heading);
print &ui_form_start("save_timegroup.cgi", "post");
my @tds = ( "width=20% style=vertical-align:top", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("timegroup");
} else {
	$col = &ui_textbox("newtimegroup", $in{'timegroup'});
	$col .= &ui_hidden("timegroup", $in{'timegroup'});
}
print &ui_columns_row([ "$icons{TIMEGROUP}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
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
