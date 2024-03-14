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
	&ui_print_header( "<img src=images/arrow.png hspace=4>$text{'edit_masq_title_create'}", $text{'title'}, "" );
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$is_masquerade = 1;
	$active = 1;
} else {
	&ui_print_header( "<img src=images/arrow.png hspace=4>$text{'edit_masq_title_edit'}", $text{'title'}, "" );
	$idx = $in{'idx'};
	%masq = $fw->GetMasquerade($idx);
	$src = $masq{'SRC'};
	$dst = $masq{'DST'};
	$service = $masq{'SERVICE'};
	$port = $masq{'PORT'};
	$is_masquerade = $masq{'MASQUERADE'} ne 'NO';
	$active = $masq{'ACTIVE'} ne 'NO';
}

$options_src = '<option>*</option>';	# All sources
$options_dst = '';
@zones = $fw->GetZoneList();
for my $k (@zones) {
	if( $k ne 'FIREWALL' ) {
		$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k.'</option>';
		# I cannot specify a zone as destination (iptables PREROUTING can have -o oprion)
		$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k.'</option>';
	}
}


@nets = $fw->GetNetList();
for my $k (@nets) {
	$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k.'</option>';
	$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k.'</option>';
}
@hosts = $fw->GetHostList();
for my $k (@hosts) {
	$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k.'</option>';
	$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k.'</option>';
}
@groups = $fw->GetGroupList();
for my $k (@groups) {
	$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k.'</option>';
	$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k.'</option>';
}




print "<br>
	<form action=\"save_masq.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_masq_title_create} : $text{edit_masq_title_edit})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\">";
if( ! $new ) { print "
			<tr>
				<td><b>#</b></td>
				<td><b><tt>$idx</tt></b></td>
			</tr>";
}
print			"<tr>
				<td><b>$text{masq_src}</b></td>
				<td><select name=\"src\">$options_src</select></td>
			</tr>
			<tr>
				<td><b>$text{masq_dst}</b></td>
				<td><select name=\"dst\">$options_dst</select></td>
			</tr>
			<tr>
				<td><b>$text{masq_service}</b></td>
				<td><br>";
				formService( $service, $port, 1 );
print			qq~	<br></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><b>$text{masq_masquerade}</b></td>
				<td>
				<input type="radio" name="masquerade" value="0" ~.($is_masquerade ? '' : 'checked').qq~>
				$text{NO}<br>
				<input type="radio" name="masquerade" value="1" ~.($is_masquerade ? 'checked' : '').qq~>
				$text{YES}
				</td>
			</tr>
			<tr>
				<td><br></td><td></td>
			</tr>
			<tr>
				<td><b>$text{masq_active}</b></td>
				<td><input type=\"checkbox\" name=\"active\" value=\"1\"~.($active ? ' checked' : '').qq~></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>~;

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
&ui_print_footer('list_nat.cgi','NAT list');
