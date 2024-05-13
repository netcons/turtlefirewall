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
$ratelimit = $in{'ratelimit'};
$newratelimit = $in{'newratelimit'};

if( $new ) {
	&ui_print_header( "<img src=images/ratelimit.png hspace=4>$text{'edit_ratelimit_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/ratelimit.png hspace=4>$text{'edit_ratelimit_title_edit'}", $text{'title'}, "" );
}

my %r = $fw->GetRateLimit($ratelimit);
my $rate = $r{'RATE'};
my $description = $r{'DESCRIPTION'};

print "<br><br>
	<form action=\"save_ratelimit.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_ratelimit_title_create'} : $text{'edit_ratelimit_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
				<td><img src=images/ratelimit.png hspace=4><b>$text{'name'}</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"ratelimit\">";
} else {
	print '		<input type="text" name="newratelimit" value="'.$ratelimit.'">';
	print '		<input type="hidden" name="ratelimit" value="'.$ratelimit.'">';
}
print			qq~</td></tr>
                   	<tr>
				<td><img src=images/rate.png hspace=4><b>$text{'rate'}</b></td>
				<td valign="top"><input type="text" name="rate" size="3" maxlength="3" value="$rate"> <i>Mbps</i></td>
			</tr>
 			<tr>
				<td><img src=images/info.png hspace=4><b>$text{'description'}</b></td>
				<td valign="top"><input type="text" name="description" size="60" value="$description"></td>
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
        print '<td align="right">'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&ui_print_footer('list_items.cgi','items list');
