#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

&header( $text{list_services_title}, '' );

LoadServices( $fw );
showServices();

print "<br><br>";
&footer('','turtle firewall index');


#============================================================================

sub showServices {
	print "<br>
		<table border width=\"100%\">
			<tr $tb>
				<th>$text{name}</th>
				<th>$text{description}</th>
			</tr>";
	my @services = $fw->GetServicesList();
	foreach $name (@services) {
		my %service = $fw->GetService($name);
		print "<tr $cb>";
		print "<td width=\"30%\">$name</td>";
		print "<td>".$service{DESCRIPTION}."</td>";
		print "</tr>";
	}
	print "</table>\n";
	#print '<a href="edit_service.cgi?new=1">create new service</a><br>';
}
