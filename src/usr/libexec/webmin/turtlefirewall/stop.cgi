#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

&ui_print_header( undef, $text{'title'}, "" );

print "<table border width=\"100%\">
       <tr $cb><td>";
print "<pre><tt>\n";
print qx{/usr/sbin/turtlefirewall --stop 2>&1};
print "</tt></pre>";
print "</td></tr></table>";

&ui_print_footer( "index.cgi", "turtle firewall index" );
