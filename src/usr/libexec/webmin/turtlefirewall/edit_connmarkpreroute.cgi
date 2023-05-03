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
	&ui_print_header( $text{'edit_connmarkpreroute_title_create'}, $text{'title'}, "" );
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
	&ui_print_header( $text{'edit_connmarkpreroute_title_edit'}, $text{'title'}, "" );
	$idx = $in{'idx'};
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

my $options_src = '';
my @items_src = ();
push @items_src, $fw->GetZoneList();
push @items_src, $fw->GetGeoipList();
push @items_src, $fw->GetNetList();
push @items_src, $fw->GetHostList();
@items_src = sort(@items_src);
for my $k (@items_src) {
	if( $k ne 'FIREWALL' ) {
		my $selected = 0;
		if( $k eq $src ) { $selected = 1; }
		$options_src .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
	}
}

my $options_dst = '';
my @items_dst = ('*');
push @items_dst, $fw->GetGeoipList();
push @items_dst, $fw->GetNetList();
push @items_dst, $fw->GetHostList();
@items_dst = sort(@items_dst);
for my $k (@items_dst) {
	my $selected = 0;
	if( $k eq $dst ) { $selected = 1; }
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
	<form action=\"save_connmarkpreroute.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_connmarkpreroute_title_create} : $text{edit_connmarkpreroute_title_edit})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\">";
if( !$new ) {
	print		"<tr>
				<td><b>#</b></td>
				<td><b><tt>$idx</tt></b></td>
			</tr>";
}
print			"<tr>
				<td><b>$text{rule_src}</b></td>
				<td><select name=\"src\">$options_src</select></td>
			</tr>
			<tr>
				<td><b>$text{rule_dst}</b></td>
				<td><select name=\"dst\">$options_dst</select> <small><i>$text{preroute_help}</i></small></td>
			</tr>
			<tr>
				<td><b>$text{rule_service}</b></td>
				<td><br>";
				formService( $service, $port, 1 );
print				"<br>
				</td>
			</tr>
			<tr>
				<td><b>$text{rule_ndpiprotocol}</b></td>
				<td><br>";
				formNdpiProtocol( $ndpi, $category, 1 );
print				"<br>
				<td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><b>$text{rule_hostname_set}</b></td>
				<td><select name=\"hostnameset\">$options_hostnameset</select></td>
			</tr>
			<tr>
				<td><b>$text{rule_risk_set}</b></td>
				<td><select name=\"riskset\">$options_riskset</select></td>
			</tr>
			<tr>
				<td><b>$text{rule_time}</b></td>
				<td><select name=\"time\">$options_time</select></td>
			</tr>
			<tr>
				<td><b>$text{rule_mark}</b></td>
				<td><input type=\"text\" name=\"mark\" value=\"$mark\" size=\"13\"></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><b>$text{rule_active}</b></td>
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
&ui_print_footer("list_manglerules.cgi?idx=$idx",'Mangle Rules list');
