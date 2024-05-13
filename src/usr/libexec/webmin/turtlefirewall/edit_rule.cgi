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
	&ui_print_header( "<img src=images/filter.png hspace=4>$text{'edit_rule_title_create'}", $text{'title'}, "" );
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
	&ui_print_header( "<img src=images/filter.png hspace=4>$text{'edit_rule_title_edit'}", $text{'title'}, "" );
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

my $options_src = '';
my $options_dst = '';
my @selected_src = split(/,/, $src);
my @selected_dst = split(/,/, $dst);
my @items = ('*');
push @items, $fw->GetZoneList();
push @items, $fw->GetGeoipList();
push @items, $fw->GetNetList();
push @items, $fw->GetHostList();
push @items, $fw->GetGroupList();
@items = sort(@items);
for my $k (@items) {
	my $selected = 0;
	for my $s (@selected_src) {
		if( $k eq $s ) {
			$selected = 1;
			last;
		}
	}
	$options_src .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
	$selected = 0;
	for my $s (@selected_dst) {
		if( $k eq $s ) {
			$selected = 1;
			last;
		}
	}
	$options_dst .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
}

my $options_hostnameset = '';
if( $hostnameset eq '' ) { $hostnameset = 'any'; }
my @hostnamesets = ('any');
push @hostnamesets, $fw->GetHostNameSetList();
for my $k (@hostnamesets) {
	my $selected = 0;
	if( $k eq $hostnameset ) { $selected = 1; }
	$options_hostnameset .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
}

my $options_riskset = '';
if( $riskset eq '' ) { $riskset = 'none'; }
my @risksets = ('none');
push @risksets, $fw->GetRiskSetList();
for my $k (@risksets) {
	my $selected = 0;
	if( $k eq $riskset ) { $selected = 1; }
	$options_riskset .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
}

my $options_ratelimit = '';
if( $ratelimit eq '' ) { $ratelimit = 'none'; }
my @ratelimits = ('none');
push @ratelimits, $fw->GetRateLimitList();
for my $k (@ratelimits) {
	my $selected = 0;
	if( $k eq $ratelimit ) { $selected = 1; }
	$options_ratelimit .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
}

my $options_time = '';
if( $time eq '' ) { $time = 'always'; }
my @times = ('always');
push @times, $fw->GetTimeList();
push @times, $fw->GetTimeGroupList();
for my $k (@times) {
	my $selected = 0;
	if( $k eq $time ) { $selected = 1; }
	$options_time .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
}

print "<br>
	<form action=\"save_rule.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_rule_title_create} : $text{edit_rule_title_edit})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\">";
if( !$new ) {
	print		"<tr>
				<td><img src=images/hash.png hspace=4><b>ID</b></td>
				<td><b>$idx</b></td>
			</tr>";
}
print			"<tr>
				<td><img src=images/zone.png hspace=4><b>$text{rule_src}</b></td>
				<td><select name=\"src\" size=\"5\" multiple>$options_src</select></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><img src=images/zone.png hspace=4><b>$text{rule_dst}</b></td>
				<td><select name=\"dst\" size=\"5\" multiple>$options_dst</select></td>
			</tr>
			<tr>
				<td><img src=images/service.png hspace=4><b>$text{rule_service}</b></td>
				<td><br>";
				formService( $service, $port, 1 );
print				"<br>
				</td>
			</tr>
			<tr>
				<td><img src=images/ndpi.png hspace=4><b>$text{rule_ndpiprotocol}</b></td>
				<td><br>";
				formNdpiProtocol( $ndpi, $category, 1 );
print				"<br>
				<td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><img src=images/hostnameset.png hspace=4><b>$text{rule_hostname_set}</b></td>
				<td><select name=\"hostnameset\">$options_hostnameset</select></td>
			</tr>
			<tr>
				<td><img src=images/riskset.png hspace=4><b>$text{rule_risk_set}</b></td>
				<td><select name=\"riskset\">$options_riskset</select></td>
			</tr>
			<tr>
				<td><img src=images/ratelimit.png hspace=4><b>$text{rule_rate_limit}</b></td>
				<td><select name=\"ratelimit\">$options_ratelimit</select></td>
			</tr>
			<tr>
				<td><img src=images/time.png hspace=4><b>$text{rule_time}</b></td>
				<td><select name=\"time\">$options_time</select></td>
			</tr>
			<tr>
				<td><img src=images/target.png hspace=4><b>$text{rule_target}</b></td>
				<td>
				<select name=\"target\">
				<option ".($target eq 'ACCEPT' ? 'SELECTED' : '').">ACCEPT</option>
				<option ".($target eq 'DROP' ? 'SELECTED' : '').">DROP</option>
				<option ".($target eq 'REJECT' ? 'SELECTED' : '').">REJECT</option>
				</select>
				</td>
			</tr>
			<tr>
				<td><img src=images/grey-eye.png hspace=4><b>$text{rule_log}</b></td>
				<td><input type=\"checkbox\" name=\"log\" value=\"1\"".($log ? ' checked' : '')."> <small><i>$text{log_help}</i></small></td>
			</tr>
			<tr>
				<td><img src=images/info.png hspace=4><b>$text{description}</b></td>
				<td><input type=\"text\" name=\"description\" value=\"$description\" size=\"60\"></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><img src=images/active.png hspace=4><b>$text{rule_active}</b></td>
				<td><input type=\"checkbox\" name=\"active\" value=\"1\"".($active ? ' checked' : '')."></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>";

print "<table width=\"100%\"><tr>";
if( $new ) {
	print '<td>'.&ui_submit( $text{'button_create'}, "new").'</td>';
} else {
	print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
	print '<td align="right">'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&ui_print_footer("list_rules.cgi?idx=$idx",'Rules list');
