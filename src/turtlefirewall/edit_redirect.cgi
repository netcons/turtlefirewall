#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

$new = $in{'new'};

if( $new ) {
	&header( $text{edit_redirect_title_create}, '' );
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$toport = '';
	$is_redirect = 1;
	$active = 1;
} else {
	&header( $text{edit_redirect_title_edit}, '' );
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
		$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k;
		# I cannot specify a zone as destination (iptables PREROUTING can have -o oprion)
		#$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k;
	}
}

# All destination
$options_dst .= '<option>*';

@nets = $fw->GetNetList();
for my $k (@nets) {
	$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k;
	$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k;
}
@hosts = $fw->GetHostList();
for my $k (@hosts) {
	$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k;
	$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k;
}
@groups = $fw->GetGroupList();
for my $k (@groups) {
	$options_src .= '<option'.($k eq $src ? ' selected' : '').'>'.$k;
	$options_dst .= '<option'.($k eq $dst ? ' selected' : '').'>'.$k;
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
				&nbsp;<i>$text{redirect_dst_help}</i>
				</td>
			</tr>
			<tr>
				<td><b>$text{redirect_service}</b></td>
				<td><br>";
				formService( $service, $port );
print			qq~	<br></td>
			</tr>
			<tr>
				<td><b>$text{redirect_redirect}</b></td>
				<td>
				<input type="radio" name="redirect" value="0" ~.($is_redirect ? '' : 'checked').qq~>
				$text{NO}<br>
				<input type="radio" name="redirect" value="1" ~.($is_redirect ? 'checked' : '').qq~>
				$text{YES}: $text{redirect_toport}
				<input type=\"text\" name=\"toport\" size=\"5\" value=\"$toport\">
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
	print '<td><input type="submit" name="new" value="'.$text{button_create}.'"></td>';
} else {
	print '<td><input type="submit" name="save" value="'.$text{button_save}.'"></td>';
	print '<td align="right"><input type="submit" name="delete" value="'.$text{button_delete}.'"></td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&footer('list_nat.cgi','Nat list');

