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
	&ui_print_header( "<img src=images/arrow.png hspace=4>$text{'edit_redirect_title_create'}", $text{'title'}, "" );
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$toport = '';
	$is_redirect = 1;
	$active = 1;
} else {
	&ui_print_header( "<img src=images/arrow.png hspace=4>$text{'edit_redirect_title_edit'}", $text{'title'}, "" );
	$idx = $in{'idx'};
	%redirect = $fw->GetRedirect($idx);
	$src = $redirect{'SRC'};
	$dst = $redirect{'DST'};
	$service = $redirect{'SERVICE'};
	$port = $redirect{'PORT'};
	$toport = $redirect{'TOPORT'};
	$is_redirect = $redirect{'REDIRECT'} ne 'NO';
	$active = $redirect{'ACTIVE'} ne 'NO';
}

$options_src = '';
$options_dst = '';
@zones = $fw->GetZoneList();
for my $k (@zones) {
	if( $k ne 'FIREWALL' ) {
		$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k.'</option>';
		# I cannot specify a zone as destination (iptables PREROUTING can have -o oprion)
		#$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k.'</option>';
	}
}

# All destination
$options_dst .= '<option>*</option>';

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
	<form action=\"save_redirect.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_redirect_title_create} : $text{edit_redirect_title_edit})."</th>
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
				<td><b>$text{redirect_src}</b></td>
				<td><select name=\"src\">$options_src</select></td>
			</tr>
			<tr>
				<td><b>$text{redirect_dst}</b></td>
				<td><select name=\"dst\">$options_dst</select>
				&nbsp;<small><i>$text{redirect_dst_help}</i></small>
				</td>
			</tr>
			<tr>
				<td><b>$text{redirect_service}</b></td>
				<td><br>";
				formService( $service, $port );
print			qq~	<br></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><b>$text{redirect_redirect}</b></td>
				<td>
				<input type="radio" name="redirect" value="0" ~.($is_redirect ? '' : 'checked').qq~>
				$text{NO}<br>
				<input type="radio" name="redirect" value="1" ~.($is_redirect ? 'checked' : '').qq~>
				$text{YES} : $text{redirect_toport} : <input type=\"text\" name=\"toport\" size=\"5\" maxlength=\"5\" value=\"$toport\">
				</td>
			</tr>
			<tr>
				<td><br></td><td></td>
			</tr>
			<tr>
				<td><b>$text{redirect_active}</b></td>
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
