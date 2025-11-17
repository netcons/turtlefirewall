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

if( $in{'zone'} eq 'FIREWALL' ) {
	redirect('list_items.cgi');
}

$new = $in{'new'};

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_zone_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_zone_title_edit'}";
}
&ui_print_header( "$icons{SHIELD}{IMAGE}$text{'index_icon_items'}", $text{'title'}, "" );

my %z = $fw->GetZone($in{'zone'});
my $if = $z{'IF'};
my $description = $z{'DESCRIPTION'};

print &ui_subheading($heading);
print &ui_form_start("save_zone.cgi", "post");
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("zone", undef, 13, 0, 13);
} else {
	$col = &ui_textbox("newzone", $in{'zone'}, 13, 0, 13);
	$col .= &ui_hidden("zone", $in{'zone'});
}
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_textbox("if", $if);
$col .= "<small><i>$text{zone_help}</i></small>";
print &ui_columns_row([ "$icons{INTERFACE}{IMAGE}<b>$text{'interface'}</b>", $col ], \@tds);
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
