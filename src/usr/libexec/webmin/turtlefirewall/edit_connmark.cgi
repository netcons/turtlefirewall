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
	&ui_print_header( "<img src=images/grey-mark.png hspace=4>$text{'edit_connmark_title_create'}", $text{'title'}, "" );
	$idx = '';
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
	&ui_print_header( "<img src=images/grey-mark.png hspace=4>$text{'edit_connmark_title_edit'}", $text{'title'}, "" );
	$idx = $in{'idx'};
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

my @selected_src = split(/,/, $src);
my @selected_dst = split(/,/, $dst);
my @items = ('*');
push @items, $fw->GetZoneList();
push @items, $fw->GetGeoipList();
push @items, $fw->GetNetList();
push @items, $fw->GetHostList();
push @items, $fw->GetGroupList();
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

print &ui_subheading($new ? $text{'edit_connmark_title_create'} : $text{'edit_connmark_title_edit'});
print &ui_form_start("save_connmark.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( !$new ) {
	$col = "<b>$idx</b>";
	print &ui_columns_row([ "<img src=images/hash.png hspace=4><b>ID</b>", $col ], \@tds);
}
$col = &ui_select("src", \@selected_src, \@items, 5, 1);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'rule_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", \@selected_dst, \@items, 5, 1);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'rule_dst'}</b>", $col ], \@tds);
$col = &formService($service, $port, 1);
print &ui_columns_row([ "<img src=images/service.png hspace=4><b>$text{'rule_service'}</b>", $col ], \@tds);
$col = &formNdpiProtocol($ndpi, $category, 1);
print &ui_columns_row([ "<img src=images/grey-ndpi.png hspace=4><b>$text{'rule_ndpi'}</b>", $col ], \@tds);
$col = &ui_select("hostnameset", $hostnameset, \@hostnamesets);
print &ui_columns_row([ "<img src=images/hostnameset.png hspace=4><b>$text{'rule_hostname_set'}</b>", $col ], \@tds);
$col = &ui_select("riskset", $riskset, \@risksets);
print &ui_columns_row([ "<img src=images/riskset.png hspace=4><b>$text{'rule_risk_set'}</b>", $col ], \@tds);
$col = &ui_select("time", $time, \@times);
print &ui_columns_row([ "<img src=images/time.png hspace=4><b>$text{'rule_time'}</b>", $col ], \@tds);
$col = &ui_textbox("mark", $mark, 13, 0, 13);
print &ui_columns_row([ "<img src=images/grey-mark.png hspace=4><b>$text{'rule_mark'}</b>", $col ], \@tds);
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
&ui_print_footer("list_manglerules.cgi?idx=$idx",'Mangle Rules list');
