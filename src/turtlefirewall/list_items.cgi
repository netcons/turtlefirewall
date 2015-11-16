#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

&header( $text{'list_items_title'}, '' );

showZone();
showNet();
showHost();
showGroup();

print "<br><br>";
&footer('','turtle firewall index');


#============================================================================

sub showZone {
	print "<br>
		<table border width=\"100%\">
			<tr $tb>
				<th width=\"30%\">".$text{'zone'}."</th>
				<th width=\"30%\">".$text{'interface'}."</th>
				<th width=\"40%\">".$text{'description'}."</th>
			</tr>";
	for my $k ($fw->GetZoneList()) {
		my %zone = $fw->GetZone($k);
		print "<tr $cb>";
		print "<td>";
		if( $k eq 'FIREWALL' ) {
			print "<i>$k</i>";
		} else {
			print "<a href=\"edit_zone.cgi?zone=$k\">$k</a>";
		}
		print "</td>";
		print "<td>".$zone{'IF'}."</td>";
		print "<td>".($zone{'DESCRIPTION'} ne '' ? $zone{'DESCRIPTION'} : '&nbsp;')."</td>";
		print "</tr>";
	}
	print "</table>\n";
	print '<a href="edit_zone.cgi?new=1">'.$text{'list_items_create_zone'}.'</a><br>';
}
sub showNet {
	print "<br>
		<table border width=\"100%\">
			<tr $tb>
				<th width=\"15%\">".$text{'net'}."</th>
				<th width=\"15%\">".$text{'netaddress'}."</th>
				<th width=\"15%\">".$text{'netmask'}."</th>
				<th width=\"15%\">".$text{'zone'}."</th>
				<th width=\"40%\">".$text{'description'}."</th>
			</tr>";
	for my $k ($fw->GetNetList()) {
		my %net = $fw->GetNet($k);
		print "<tr $cb>";
		print "<td><a href=\"edit_net.cgi?net=$k\">$k</a></td>";
		print "<td>".$net{'IP'}."</td>";
		print "<td>".$net{'NETMASK'}."</td>";
		print "<td>".$net{'ZONE'}."</td>";
		print "<td>".($net{'DESCRIPTION'} ne '' ? $net{'DESCRIPTION'} : '&nbsp;')."</td>";
		print "</tr>";
	}
	print "</table>\n";
	print '<a href="edit_net.cgi?new=1">'.$text{'list_items_create_net'}.'</a><br>';
}
sub showHost {
	print "<br>
		<table border width=\"100%\">
			<tr $tb>
				<th width=\"15%\">".$text{'host'}."</th>
				<th width=\"15%\">".$text{'hostaddress'}."</th>
				<th width=\"15%\">".$text{'macaddress'}."</th>
				<th width=\"15%\">".$text{'zone'}."</th>
				<th width=\"40%\">".$text{'description'}."</th>
			</tr>";
	for my $k ($fw->GetHostList()) {
		my %host = $fw->GetHost($k);
		print "<tr $cb>";
		print "<td><a href=\"edit_host.cgi?host=$k\">$k</a></td>";
		print "<td>".$host{'IP'}."</td>";
		print "<td>".$host{'MAC'}."</td>";
		print "<td>".$host{'ZONE'}."</td>";
		print "<td>".($host{'DESCRIPTION'} ne '' ? $host{'DESCRIPTION'} : '&nbsp;')."</td>";
		print "</tr>";
	}
	print "</table>\n";
	print '<a href="edit_host.cgi?new=1">'.$text{'list_items_create_host'}.'</a><br>';
}
sub showGroup {
	print "<br>
		<table border width=\"100%\">
			<tr $tb>
				<th width=\"30%\">".$text{'group'}."</th>
				<th width=\"30%\">".$text{'groupitems'}."</th>
				<th width=\"40%\">".$text{'description'}."</th>
			</tr>";
	for my $k ($fw->GetGroupList()) {
		my %group = $fw->GetGroup($k);
		print "<tr $cb>";
		print "<td valign=\"top\"><a href=\"edit_group.cgi?group=$k\">$k</a></td>";
		print "<td valign=\"top\">";
		for my $item (@{$group{ITEMS}}) {
			print "$item<br>";
		}
		print "</td>";
		print "<td valign=\"top\">".($group{'DESCRIPTION'} ne '' ? $group{'DESCRIPTION'} : '&nbsp;')."</td>";
		print "</tr>";
	}
	print "</table>\n";
	print '<a href="edit_group.cgi?new=1">'.$text{'list_items_create_group'}.'</a><br>';
}
