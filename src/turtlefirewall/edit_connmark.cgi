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

my $nConnmarks = $fw->GetConnmarksCount();

$new = $in{'new'};

if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_connmark_title_create'}";
	$nConnmarks++;
	$idx = $nConnmarks;
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
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_connmark_title_edit'}";
	$idx = $in{'idx'};
	$newIdx = '';
	%rule = $fw->GetConnmark($idx);
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
for( my $i=1; $i<=$nConnmarks; $i++ ) { push @idxs, $i; }

my @selected_src = split(/,/, $src);
my @selected_dst = split(/,/, $dst);
my @items = ('*');
push @items, $fw->GetZoneList();
push @items, $fw->GetGeoipList();
push @items, $fw->GetNetList();
push @items, $fw->GetHostList();
push @items, $fw->GetGroupList();
push @items, $fw->GetIPSetList();
@items = sort(@items);

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
print &ui_form_start("save_connmark.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
$col = &ui_select("newIdx", $idx, \@idxs);
print &ui_columns_row([ "$icons{ID}{IMAGE}<b>ID</b>", $col ], \@tds);
$col = &ui_select("src", \@selected_src, \@items, 5, 1);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'rule_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", \@selected_dst, \@items, 5, 1);
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
&ui_print_footer("list_manglerules.cgi?table=connmark&idx=$idx",'Mangle Rules list');
