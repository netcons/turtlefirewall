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

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_net_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_net_title_edit'}";
}
&ui_print_header( $heading, $text{'title'}, "" );

my $net = $in{'net'};
my $newnet = $in{'newnet'};
my %n = $fw->GetNet($net);
my $ip = $n{'IP'};
my $netmask = $n{'NETMASK'};
my $zone = $n{'ZONE'};
my $description = $n{'DESCRIPTION'};

my @zones = grep(!/FIREWALL/, $fw->GetZoneList());

print &ui_subheading($heading);
print &ui_form_start("save_net.cgi", "post");
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("net");
} else {
	$col = &ui_textbox("newnet", $in{'net'});
	$col .= &ui_hidden("net", $in{'net'});
}
print &ui_columns_row([ "$icons{NET}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_textbox("ip", $ip, 15, 0, 15);
print &ui_columns_row([ "$icons{ADDRESS}{IMAGE}<b>$text{'netaddress'}</b>", $col ], \@tds);
$col = &ui_textbox("netmask", $netmask, 15, 0, 15);
print &ui_columns_row([ "$icons{NETMASK}{IMAGE}<b>$text{'netmask'}</b>", $col ], \@tds);
$col = &ui_select("zone", $zone, \@zones);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'zone'}</b>", $col ], \@tds);
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
