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
	&ui_print_header( "<img src=images/host.png hspace=4>$text{'edit_host_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/host.png hspace=4>$text{'edit_host_title_edit'}", $text{'title'}, "" );
}

$host = $in{'host'};
%h = $fw->GetHost($host);
$ip = $h{'IP'};
$mac = $h{'MAC'};
$zone = $h{'ZONE'};
$description = $h{'DESCRIPTION'};

$options_zone = '';
@zones = $fw->GetZoneList();
for my $k (@zones) {
	if( $k ne 'FIREWALL' ) {
		$options_zone .= '<option'.($k eq $zone ? ' selected' : '').'>'.$k.'</option>';
	}
}

print "<br><br>
	<form action=\"save_host.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_host_title_create'} : $text{'edit_host_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
				<td><img src=images/host.png hspace=4><b>$text{'name'}</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"host\">";
} else {
	print '		<input type="text" name="newhost" value="'.$in{'host'}.'">';
	print '		<input type="hidden" name="host" value="'.$in{'host'}.'">';
}
print			qq~</td></tr>
			<tr>
				<td><img src=images/address.png hspace=4><b>$text{'hostaddress'}</b></td>
				<td><input type="text" name="ip" value="$ip" size="15"> <small><i>$text{host_help}</i></small></td>
			</tr>
			<tr>
				<td><img src=images/address.png hspace=4><b>$text{'macaddress'}</b></td>
				<td><input type="text" name="mac" value="$mac" size="17"> <small><i>$text{mac_help}</i></small></td>
			</tr>
			<tr>
				<td><img src=images/zone.png hspace=4><b>$text{'zone'}</b></td>
				<td><select name="zone">$options_zone</select></td>
			</tr>
			<tr>
				<td><img src=images/info.png hspace=4><b>$text{'description'}</b></td>
				<td><input type="text" size="60" name="description" value="$description"></td>
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
        print '<td style=text-align:right>'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&ui_print_footer('list_items.cgi','items list');

