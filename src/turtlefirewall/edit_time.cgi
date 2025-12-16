#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();

$new = $in{'new'};
$time = $in{'time'};
$newtime = $in{'newtime'};

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_time_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_time_title_edit'}";
}
&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_items'}", $text{'title'}, "" );

my @aWeekdays = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun');

my %t = $fw->GetTime($time);
my $weekdays = $t{'WEEKDAYS'};
my $timestart = $t{'TIMESTART'};
my $timestop = $t{'TIMESTOP'};
my $description = $t{DESCRIPTION};

my @timeWeekdays = split(/,/, $weekdays);
my %aSelectedWeekdays = ();
foreach my $k (@timeWeekdays) {
	$aSelectedWeekdays{$k} = 1;
}

print &ui_subheading($heading);
print &ui_form_start("save_time.cgi", "post");
my @tds = ( "width=20% style=vertical-align:top", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("time");
} else {
	$col = &ui_textbox("newtime", $in{'time'});
	$col .= &ui_hidden("time", $in{'time'});
}
print &ui_columns_row([ "$icons{TIME}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = "<table width=100%><tr>";
foreach my $i (@aWeekdays) {
	$col .= "<td><nobr>";
	$col .= &ui_checkbox("item_$i", 1, $i, $aSelectedWeekdays{$i} ? 1 : 0);
	$col .= "</nobr></td>";
}
$col .= "</tr></table>";
print &ui_columns_row([ "$icons{ITEM}{IMAGE}<b>$text{'timeitems'}</b>", $col ], \@tds);
$col = &ui_textbox("timestart", $timestart, 5, 0, 5);
print &ui_columns_row([ "$icons{TIMESTART}{IMAGE}<b>$text{'timestart'}</b>", $col ], \@tds);
$col = &ui_textbox("timestop", $timestop, 5, 0, 5);
print &ui_columns_row([ "$icons{TIMESTOP}{IMAGE}<b>$text{'timestop'}</b>", $col ], \@tds);
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
