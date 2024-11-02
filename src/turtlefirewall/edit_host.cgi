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
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_host_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_host_title_edit'}";
}
&ui_print_header( $heading, $text{'title'}, "" );

my $host = $in{'host'};
my %h = $fw->GetHost($host);
my $ip = $h{'IP'};
my $mac = $h{'MAC'};
my $zone = $h{'ZONE'};
my $description = $h{'DESCRIPTION'};

my @zones = grep(!/FIREWALL/, $fw->GetZoneList());

print &ui_subheading($heading);
print &ui_form_start("save_host.cgi", "post");
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("host");
} else {
	$col = &ui_textbox("newhost", $in{'host'});
	$col .= &ui_hidden("host", $in{'host'});
}
print &ui_columns_row([ "$icons{HOST}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_textbox("ip", $ip, 15, 0, 15);
$col .= "<small><i>$text{host_help}</i></small>";
print &ui_columns_row([ "$icons{ADDRESS}{IMAGE}<b>$text{'hostaddress'}</b>", $col ], \@tds);
$col = &ui_textbox("mac", $mac, 17, 0, 17);
$col .= "<small><i>$text{mac_help}</i></small>";
print &ui_columns_row([ "$icons{ADDRESS}{IMAGE}<b>$text{'macaddress'}</b>", $col ], \@tds);
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
