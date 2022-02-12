#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'turtlefirewall-lib.pl';

$new = $in{'new'};

if( $new ) {
	&ui_print_header( $text{'edit_connmark_title_create'}, $text{'title'}, "" );
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$ndpi = '';
	$set = '';
	$time = '';
	$mark = '';
	$active = 1;
} else {
	&ui_print_header( $text{'edit_connmark_title_edit'}, $text{'title'}, "" );
	$idx = $in{'idx'};
	%rule = $fw->GetConnmark($idx);
	$src = $rule{'SRC'};
	$dst = $rule{'DST'};
	$service = $rule{'SERVICE'};
	$port = $rule{'PORT'};
	$ndpi = $rule{'NDPI'};
	$set = $rule{'SET'};
	$time = $rule{'TIME'};
	$mark = $rule{'MARK'};
	$active = $rule{'ACTIVE'} ne 'NO';
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
if( $set eq '' ) { $set = 'any'; }
my @sets = ('any');
push @sets, $fw->GetHostNameSetList();
for my $k (@sets) {
	my $selected = 0;
	if( $k eq $set ) { $selected = 1; }
	$options_hostnameset .= '<option'.($selected ? ' selected' : '').'>'.$k.'</option>';
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
	<form action=\"save_connmark.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_connmark_title_create} : $text{edit_connmark_title_edit})."</th>
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
				<td><select name=\"dst\">$options_dst</select></td>
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
				formNdpiProtocol( $ndpi, 1 );
print				"<br>
				<td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><b>$text{rule_hostname_set}</b></td>
				<td><select name=\"set\">$options_hostnameset</select> <small><i>$text{hostname_help}</i></small></td>
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
