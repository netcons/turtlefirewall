#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();

&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_backup'}", $text{'title'}, "" );

print qq~<br/>
<table border="0" width="100%">
<tr $tb>
	<th>$text{'backup_backuptitle'}</th>
</tr>
<tr $cb>
	<td style=text-align:center>
	<br/>~;
print   &ui_form_start("download.cgi", "post");
print   &ui_submit($text{'backup_index_download'});
print   &ui_form_end();
print qq~<br/><br/>
	</td>
</tr>
</table>

<table border="0" width="100%">
<tr $tb>
	<th>$text{'backup_restoretitle'}</th>
</tr>
<tr $cb>
	<td style=text-align:center>
	<br/>~;
print   &ui_form_start("restore.cgi", "form-data");
print 	&ui_upload("backup", 40);
print 	&ui_submit($text{'backup_index_restore'});
print   &ui_form_end();
print qq~<br/><br/>
	<br/>
	</td>
</tr>
</table><br>~;

&ui_print_footer('index.cgi',$text{'index'});
