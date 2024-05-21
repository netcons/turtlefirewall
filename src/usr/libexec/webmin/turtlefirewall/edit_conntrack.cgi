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

if( $new ) {
	&ui_print_header( "<img src=images/grey-helper.png hspace=4>$text{'edit_conntrack_title_create'}", $text{'title'}, "" );
	$idx = '';
	$src = 'FIREWALL';
	$dst = '';
	$service = '';
	$port = '';
	$helper = '';
	$active = 1;
} else {
	&ui_print_header( "<img src=images/grey-helper.png hspace=4>$text{'edit_conntrack_title_edit'}", $text{'title'}, "" );
	$idx = $in{'idx'};
	%rule = $fw->GetConntrack($idx);
	$src = $rule{'SRC'};
	$dst = $rule{'DST'};
	$service = $rule{'SERVICE'};
	$port = $rule{'PORT'};
	$helper = $rule{'HELPER'};
	$active = $rule{'ACTIVE'} ne 'NO';
}

my @items_dst = ('*');
push @items_dst, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_dst, $fw->GetGeoipList();
push @items_dst, $fw->GetNetList();
push @items_dst, $fw->GetHostList();
push @items_dst, $fw->GetGroupList();
@items_dst = sort(@items_dst);

my @services = ('tcp','udp');

my @helpers = ('amanda','ftp','irc','netbios-ns','pptp','RAS','sane','sip','snmp','tftp','Q.931');

print &ui_subheading($new ? $text{'edit_conntrack_title_create'} : $text{'edit_conntrack_title_edit'});
print &ui_form_start("save_conntrack.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( !$new ) {
	$col = "<b>$idx</b>";
	print &ui_columns_row([ "<img src=images/hash.png hspace=4><b>ID</b>", $col ], \@tds);
}
$col = "$src";
$col .= &ui_hidden("src", $src);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'rule_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", $dst, \@items_dst);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'rule_dst'}</b>", $col ], \@tds);
$col = &ui_select("service", $service, \@services);
$col .= "$text{rule_port} : ";
$col .= &ui_textbox("port", $port, 11, 0, 11);
$col .= "<small><i>$text{port_help}</i></small>";
print &ui_columns_row([ "<img src=images/service.png hspace=4><b>$text{'rule_service'}</b>", $col ], \@tds);
$col = &ui_select("helper", $helper, \@helpers);
print &ui_columns_row([ "<img src=images/grey-helper.png hspace=4><b>$text{'rule_helper'}</b>", $col ], \@tds);
$col = &ui_checkbox("active", 1, undef, $active ? 1 : 0);
print &ui_columns_row([ "<img src=images/active.png hspace=4><b>$text{'rule_active'}</b>", $col ], \@tds);
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
&ui_print_footer("list_rawrules.cgi?idx=$idx",'Raw Rules list');
