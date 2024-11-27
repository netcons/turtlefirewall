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

my $nConnmarkPreroutes = $fw->GetConnmarkPreroutesCount();

$new = $in{'new'};

if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_connmarkpreroute_title_create'}";
	$nConnmarkPreroutes++;
	$idx = $nConnmarkPreroutes;
	$newIdx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$ndpi = '';
	$category = '';
	$hostnameset = '';
	$riskset = '';
	$time = '';
	$mark = '';
	$active = 1;
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_connmarkpreroute_title_edit'}";
	$idx = $in{'idx'};
	$newIdx = '';
	%rule = $fw->GetConnmarkPreroute($idx);
	$src = $rule{'SRC'};
	$dst = $rule{'DST'};
	$service = $rule{'SERVICE'};
	$port = $rule{'PORT'};
	$ndpi = $rule{'NDPI'};
	$category = $rule{'CATEGORY'};
	$hostnameset = $rule{'HOSTNAMESET'};
	$riskset = $rule{'RISKSET'};
	$time = $rule{'TIME'};
	$mark = $rule{'MARK'};
	$active = $rule{'ACTIVE'} ne 'NO';
}
&ui_print_header( $heading, $text{'title'}, "" );

my @idxs = ();
for( my $i=1; $i<=$nConnmarkPreroutes; $i++ ) { push @idxs, $i; }

my @items_src = ();
push @items_src, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_src, $fw->GetGeoipList();
push @items_src, $fw->GetNetList();
push @items_src, $fw->GetHostList();
push @items_src, $fw->GetIPSetList();
@items_src = sort(@items_src);

my @items_dst = ('*');
push @items_dst, $fw->GetGeoipList();
push @items_dst, $fw->GetNetList();
push @items_dst, $fw->GetHostList();
push @items_dst, $fw->GetIPSetList();
@items_dst = sort(@items_dst);

if( $hostnameset eq '' ) { $hostnameset = 'any'; }
my @hostnamesets = ('any');
push @hostnamesets, $fw->GetHostNameSetList();

if( $riskset eq '' ) { $riskset = 'none'; }
my @risksets = ('none');
push @risksets, $fw->GetRiskSetList();

if( $time eq '' ) { $time = 'always'; }
my @times = ('always');
push @times, $fw->GetTimeList();
push @times, $fw->GetTimeGroupList();

print &ui_subheading($heading);
print &ui_form_start("save_connmarkpreroute.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
$col = &ui_select("newIdx", $idx, \@idxs, 1);
print &ui_columns_row([ "$icons{ID}{IMAGE}<b>ID</b>", $col ], \@tds);
$col = &ui_select("src", $src, \@items_src);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'rule_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", $dst, \@items_dst);
$col .= "<small><i>$text{preroute_help}</i></small>";
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'rule_dst'}</b>", $col ], \@tds);
$col = &formService($service, $port, 1);
print &ui_columns_row([ "$icons{SERVICE}{IMAGE}<b>$text{'rule_service'}</b>", $col ], \@tds);
$col = &formNdpiProtocol($ndpi, $category, 1);
print &ui_columns_row([ "$icons{NDPISERVICE}{IMAGE}<b>$text{'rule_ndpi'}</b>", $col ], \@tds);
$col = &ui_select("hostnameset", $hostnameset, \@hostnamesets);
print &ui_columns_row([ "$icons{HOSTNAMESET}{IMAGE}<b>$text{'rule_hostname_set'}</b>", $col ], \@tds);
$col = &ui_select("riskset", $riskset, \@risksets);
print &ui_columns_row([ "$icons{RISKSET}{IMAGE}<b>$text{'rule_risk_set'}</b>", $col ], \@tds);
$col = &ui_select("time", $time, \@times);
print &ui_columns_row([ "$icons{TIME}{IMAGE}<b>$text{'rule_time'}</b>", $col ], \@tds);
$col = &ui_textbox("mark", $mark, 13, 0, 13);
print &ui_columns_row([ "$icons{MARK}{IMAGE}<b>$text{'rule_mark'}</b>", $col ], \@tds);
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
&ui_print_footer("list_manglerules.cgi?idx=$idx",'Mangle Rules list');
