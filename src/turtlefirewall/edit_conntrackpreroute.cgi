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

my $nConntrackPreroutes = $fw->GetConntrackPreroutesCount();

$new = $in{'new'};

if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_conntrackpreroute_title_create'}";
	$nConntrackPreroutes++;
	$idx = $nConntrackPreroutes;
	$newIdx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$helper = '';
	$active = 1;
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_conntrackpreroute_title_edit'}";
	$idx = $in{'idx'};
	$newIdx = '';
	%rule = $fw->GetConntrackPreroute($idx);
	$src = $rule{'SRC'};
	$dst = $rule{'DST'};
	$service = $rule{'SERVICE'};
	$port = $rule{'PORT'};
	$helper = $rule{'HELPER'};
	$active = $rule{'ACTIVE'} ne 'NO';
}
&ui_print_header( $heading, $text{'title'}, "" );

my @idxs = ();
for( my $i=1; $i<=$nConntrackPreroutes; $i++ ) { push @idxs, $i; }

my @items_src = ('*');
push @items_src, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_src, $fw->GetGeoipList();
push @items_src, $fw->GetNetList();
push @items_src, $fw->GetHostList();
push @items_src, $fw->GetGroupList();
push @items_src, $fw->GetIPSetList();
@items_src = sort(@items_src);

my @items_dst = ('*');
push @items_dst, $fw->GetGeoipList();
push @items_dst, $fw->GetNetList();
push @items_dst, $fw->GetHostList();
push @items_dst, $fw->GetIPSetList();
@items_dst = sort(@items_dst);

my @services = ('tcp','udp');

my @helpers = ('amanda','ftp','irc','netbios-ns','pptp','RAS','sane','sip','snmp','tftp','Q.931');

print &ui_subheading($heading);
print &ui_form_start("save_conntrackpreroute.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
$col = &ui_select("newIdx", $idx, \@idxs);
print &ui_columns_row([ "$icons{ID}{IMAGE}<b>ID</b>", $col ], \@tds);
$col = &ui_select("src", $src, \@items_src);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'rule_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", $dst, \@items_dst);
$col .= "<small><i>$text{preroute_help}</i></small>";
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'rule_dst'}</b>", $col ], \@tds);
$col = &ui_select("service", $service, \@services);
$col .= "$text{rule_port} : ";
$col .= &ui_textbox("port", $port, 11, 0, 11);
$col .= "<small><i>$text{port_help}</i></small>";
print &ui_columns_row([ "$icons{SERVICE}{IMAGE}<b>$text{'rule_service'}</b>", $col ], \@tds);
$col = &ui_select("helper", $helper, \@helpers);
print &ui_columns_row([ "$icons{NDPISERVICE}{IMAGE}<b>$text{'rule_helper'}</b>", $col ], \@tds);
$col = &ui_checkbox("active", 1, undef, $active ? 1 : 0);
print &ui_columns_row([ "$icons{ACTIVE}{IMAGE}<b>$text{'rule_active'}</b>", $col ], \@tds);
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
&ui_print_footer("list_rawrules.cgi?table=conntrackpreroute&idx=$idx",'Raw Rules list');
