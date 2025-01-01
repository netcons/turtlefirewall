#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';
&ReadParse();

$new = $in{'new'};

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_ipset_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_ipset_title_edit'}";
}
&ui_print_header( $heading, $text{'title'}, "" );

my $ipset = $in{'ipset'};
my $newipset = $in{'newipset'};
my %i = $fw->GetIPSet($ipset);
my $ip = $i{'IP'};
my $zone = $i{'ZONE'};
my $description = $i{'DESCRIPTION'};

my @ips = $fw->GetAddressListList();

my @zones = grep(!/FIREWALL/, $fw->GetZoneList());

print &ui_subheading($heading);
print &ui_form_start("save_ipset.cgi", "post");
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("ipset");
} else {
	$col = &ui_textbox("newipset", $in{'ipset'});
	$col .= &ui_hidden("ipset", $in{'ipset'});
}
print &ui_columns_row([ "$icons{IPSET}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_select("ip", $ip, \@ips);
print &ui_columns_row([ "$icons{ADDRESS}{IMAGE}<b>$text{'addresslist'}</b>", $col ], \@tds);
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
