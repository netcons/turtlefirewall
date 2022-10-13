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
	&ui_print_header( $text{'edit_conntrackpreroute_title_create'}, $text{'title'}, "" );
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$helper = '';
	$active = 1;
} else {
	&ui_print_header( $text{'edit_conntrackpreroute_title_edit'}, $text{'title'}, "" );
	$idx = $in{'idx'};
	%rule = $fw->GetConntrackPreroute($idx);
	$src = $rule{'SRC'};
	$dst = $rule{'DST'};
	$service = $rule{'SERVICE'};
	$port = $rule{'PORT'};
	$helper = $rule{'HELPER'};
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

my $options_service = '';
my @services = ('tcp','udp');
for my $k (@services) {
	$options_service .= '<option'.($k eq $service ? ' selected' : '').'>'.$k.'</option>';
}

my $options_helper = '';
my @helpers = ('amanda','ftp','irc','netbios-ns','pptp','RAS','sane','sip','snmp','tftp','Q.931');
for my $k (@helpers) {
	$options_helper .= '<option'.($k eq $helper ? ' selected' : '').'>'.$k.'</option>';
}

print "<br>
	<form action=\"save_conntrackpreroute.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_conntrackpreroute_title_create} : $text{edit_conntrackpreroute_title_edit})."</th>
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
				<td><select name=\"service\">$options_service</select>
				$text{rule_port} : <input type=\"TEXT\" name=\"port\" value=\"$port\" size=\"5\"> <small><i>$text{port_help}</i></small></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><b>$text{rule_helper}</b></td>
				<td><select name=\"helper\">$options_helper</select></td>
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
&ui_print_footer("list_rawrules.cgi?idx=$idx",'Raw Rules list');
