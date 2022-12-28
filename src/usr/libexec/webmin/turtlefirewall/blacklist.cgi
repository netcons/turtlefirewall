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

&ui_print_header( $text{'blacklist_title'}, $text{'title'}, "" );

print '<table width="100%"><tr>';
print '<td>';
print &ui_form_start("blacklist.cgi", "post");
print &ui_submit( $text{'index_searchblacklist'}, "searchblacklist");
print &ui_form_end();
print '</td>';
print '<td align="right">';
print &ui_form_start("blacklist.cgi", "post");
print &ui_submit( $text{'index_updateblacklist'}, "updateblacklist");
print &ui_form_end();
print '</td>';
print '</tr></table>';

if( $in{searchblacklist} ne '' ) {
	print "<br>";
	print "<br><table border width=\"100%\">
		<tr $tb><th>blacklist</th></tr>
		<tr $cb><td>";
	print "<pre><tt><small>";
	print qx{ipset list blacklist 2>&1};
	print "</small></tt></pre>";
	print "</td></tr></table>";
}

if( $in{updateblacklist} ne '' ) {
	print "<br><br>";
	print "<table border width=\"100%\">
		<tr $cb><td>";
	print "<pre><tt>\n";
	print qx{/usr/sbin/turtleblacklist --all 2>&1};
	print "</tt></pre>";
	print "</td></tr></table>";
}

print "<br>";

&ui_print_footer('','turtle firewall index');
