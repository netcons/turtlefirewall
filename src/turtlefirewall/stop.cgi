#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

@output = ();
foreach my $l (qx{/usr/sbin/turtlefirewall --stop 2>&1}) {
	push @output, $fw->_clean($l);
}

&ui_print_header( undef, $text{'title'}, "" );

print "<table border width=100%>
       <tr $cb><td>";
print "<pre>\n";
print @output;
print "</pre>";
print "</td></tr></table>";

&ui_print_footer('index.cgi',$text{'index'});
