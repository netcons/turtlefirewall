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
	&ui_print_header( "<img src=images/grey-nat.png hspace=4>$text{'edit_nat_title_create'}", $text{'title'}, "" );
	$idx = '';
	$virtual = '';
	$real = '';
	$service = '';
	$port = '';
        $toport = '';
	$active = 1;
} else {
	&ui_print_header( "<img src=images/grey-nat.png hspace=4>$text{'edit_nat_title_edit'}", $text{'title'}, "" );
	$idx = $in{'idx'};
	%nat = $fw->GetNat($idx);
	$virtual = $nat{'VIRTUAL'};
	$real = $nat{'REAL'};
	$service = $nat{'SERVICE'};
	$port = $nat{'PORT'};
        $toport = $nat{'TOPORT'};
	$active = $nat{'ACTIVE'} ne 'NO';
}


$options_virtual = '';
$options_real = '';
@zones = $fw->GetZoneList();
@hosts = $fw->GetHostList();
for my $k (@hosts) {
	$options_virtual .= '<option'.($k eq $virtual ? ' selected' : '').'>'.$k.'</option>';
	$options_real .= '<option'.($k eq $real ? ' selected' : '').'>'.$k.'</option>';
}
for my $k (@zones) {
	if( $k ne 'FIREWALL' ) {
		my %zone = $fw->GetZone($k);
		$options_virtual .= '<option'.($k eq $virtual ? ' selected' : '').'>'.$k.' ('.$zone{IF}.')</option>';
	}
}


print "<br>
	<form action=\"save_nat.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_nat_title_create} : $text{edit_nat_title_edit})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\">";
if( ! $new ) { print "
			<tr>
				<td><img src=images/hash.png hspace=4><b>ID</b></td>
				<td><b>$idx</b></td>
			</tr>";
}
print "			<tr>
				<td width=\"20%\"><b><nobr><img src=images/zone.png hspace=4>$text{virtual_host}<nobr></b></td>
				<td><select name=\"virtual\">$options_virtual</select></td>
			</tr>
			<tr>
				<td><img src=images/host.png hspace=4><b>$text{real_host}</b></td>
				<td><select name=\"real\">$options_real</select></td>
			</tr>
			<tr>
				<td><img src=images/service.png hspace=4><b>$text{nat_service}</b></td>
				<td><br>";
				formService( $service, $port, 1 );
print "				<br></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><img src=images/grey-nat.png hspace=4><b>$text{nat}</b></td>
			       	<td>$text{YES} : $text{real_port} $text{nat_port} : <input type=\"text\" name=\"toport\" size=\"5\" maxlength=\"5\" value=\"$toport\"></td>
			</tr>
			<tr>
                                <td><br></td><td></td>
                        </tr>
			<tr>
				<td><img src=images/active.png hspace=4><b>$text{nat_active}</b></td>
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
&ui_print_footer('list_nat.cgi','NAT list');
