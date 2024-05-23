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
	$heading = "<img src=images/create.png hspace=4>$text{'edit_rule_title_create'}";
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$ndpi = '';
	$category = '';
	$hostnameset = '';
	$riskset = '';
	$ratelimit = '';
	$time = '';
	$target = '';
	$active = 1;
	$log = '';
	$description = '';
} else {
	$heading = "<img src=images/edit.png hspace=4>$text{'edit_rule_title_edit'}";
	$idx = $in{'idx'};
	%rule = $fw->GetRule($idx);
	$src = $rule{'SRC'};
	$dst = $rule{'DST'};
	$service = $rule{'SERVICE'};
	$port = $rule{'PORT'};
	$ndpi = $rule{'NDPI'};
	$category = $rule{'CATEGORY'};
	$hostnameset = $rule{'HOSTNAMESET'};
	$riskset = $rule{'RISKSET'};
	$ratelimit = $rule{'RATELIMIT'};
	$time = $rule{'TIME'};
	$target = $rule{'TARGET'};
	$active = $rule{'ACTIVE'} ne 'NO';
	$log = $rule{'LOG'} eq 'YES';
	$description = $rule{'DESCRIPTION'};
}
&ui_print_header( $heading, $text{'title'}, "" );

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

if( $ratelimit eq '' ) { $ratelimit = 'none'; }
my @ratelimits = ('none');
push @ratelimits, $fw->GetRateLimitList();

if( $time eq '' ) { $time = 'always'; }
my @times = ('always');
push @times, $fw->GetTimeList();
push @times, $fw->GetTimeGroupList();

my @targets = ( 'ACCEPT', 'DROP', 'REJECT' );

print &ui_subheading($heading);
print &ui_form_start("save_rule.cgi", "post");
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
$col = &ui_select("ratelimit", $ratelimit, \@ratelimits);
print &ui_columns_row([ "<img src=images/ratelimit.png hspace=4><b>$text{'rule_rate_limit'}</b>", $col ], \@tds);
$col = &ui_select("time", $time, \@times);
print &ui_columns_row([ "<img src=images/time.png hspace=4><b>$text{'rule_time'}</b>", $col ], \@tds);
$col = &ui_select("target", $target, \@targets);
print &ui_columns_row([ "<img src=images/target.png hspace=4><b>$text{'rule_target'}</b>", $col ], \@tds);
$col = &ui_checkbox("log", 1, undef, $log ? 1 : 0);
$col .= "<small><i>$text{log_help}</i></small>";
print &ui_columns_row([ "<img src=images/grey-eye.png hspace=4><b>$text{'rule_log'}</b>", $col ], \@tds);
$col = &ui_textbox("description", $description, 60, 0, 60);
print &ui_columns_row([ "<img src=images/info.png hspace=4><b>$text{'description'}</b>", $col ], \@tds);
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
&ui_print_footer("list_rules.cgi?idx=$idx",'Rules list');
