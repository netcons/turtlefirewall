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

my $heading = '';
if( $new ) {
	$heading = "<img src=images/create.png hspace=4>$text{'edit_net_title_create'}";
} else {
	$heading = "<img src=images/edit.png hspace=4>$text{'edit_net_title_edit'}";
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
print &ui_columns_row([ "<img src=images/net.png hspace=4><b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_textbox("ip", $ip);
print &ui_columns_row([ "<img src=images/address.png hspace=4><b>$text{'netaddress'}</b>", $col ], \@tds);
$col = &ui_textbox("netmask", $netmask, 15, 0, 15);
print &ui_columns_row([ "<img src=images/mask.png hspace=4><b>$text{'netmask'}</b>", $col ], \@tds);
$col = &ui_select("zone", $zone, \@zones);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'zone'}</b>", $col ], \@tds);
$col = &ui_textbox("description", $description, 60, 0, 60);
print &ui_columns_row([ "<img src=images/info.png hspace=4><b>$text{'description'}</b>", $col ], \@tds);
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
