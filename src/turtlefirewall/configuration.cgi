#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';

&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_configuration'}", $text{'title'}, "" );

print '<table width="100%"><tr>';
print '<td>';
print &ui_form_start("backup.cgi", "post");
print &ui_submit($text{'configuration_index_download'});
print &ui_form_end();
print '</td>';
print '<td>';
print &ui_form_start("restore.cgi", "form-data");
print &ui_upload("backup", 40);
print &ui_submit($text{'configuration_index_restore'});
print &ui_form_end();
print '</td>';
print '</tr></table>';

print "<br>\n";

&ui_print_footer('index.cgi',$text{'index'});
