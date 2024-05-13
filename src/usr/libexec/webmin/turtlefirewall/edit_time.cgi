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
$time = $in{'time'};
$newtime = $in{'newtime'};

if( $new ) {
	&ui_print_header( "<img src=images/time.png hspace=4>$text{'edit_time_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/time.png hspace=4>$text{'edit_time_title_edit'}", $text{'title'}, "" );
}

@aWeekdays = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun');

my %t = $fw->GetTime($time);
my $weekdays = $t{'WEEKDAYS'};
my $timestart = $t{'TIMESTART'};
my $timestop = $t{'TIMESTOP'};
my $description = $t{DESCRIPTION};

my @timeWeekdays = split(/,/, $weekdays);
%aSelectedWeekdays = ();
foreach my $k (@timeWeekdays) {
	$aSelectedWeekdays{$k} = 1;
}

print "<br><br>
	<form action=\"save_time.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_time_title_create'} : $text{'edit_time_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
				<td valign=\"top\"><img src=images/time.png hspace=4><b>$text{'name'}</b></td>
			<td valign=\"top\">";
if( $new ) {
	print "		<input type=\"text\" name=\"time\">";
} else {
	print '		<input type="text" name="newtime" value="'.$time.'">';
	print '		<input type="hidden" name="time" value="'.$time.'">';
}
print			'</td></tr>
			<tr>
				<td valign="top"><img src=images/item.png hspace=4><b>'.$text{'timeitems'}.'</b></td>
				<td valign="top">
					<table width="100%">';

my $col = 0;
foreach my $i (@aWeekdays) {
	if( $col == 0 ) { print "<tr>"; }
	print "<td width=\"10%\"><nobr><input type=\"checkbox\" name=\"item_$i\" value=\"1\" ";
	print ($aSelectedWeekdays{$i} ? ' checked' : '');
	print "> $i</nobr></td>";
	if( ++$col == 7 ) {
		$col = 0;
		print "</tr>";
	}
}
if( $col < 6 ) { print "</tr>"; }

print					'</table>
				</td>
			</tr>';

print 			'<tr><td valign="top"><img src=images/stopwatch.png hspace=4><b>'.$text{'timestart'}.'</b></td>';
print			'<td valign="top"><input type="text" name="timestart" size="5" value="'.$timestart.'"></td>';
print			'</tr>';

print 			'<tr><td valign="top"><img src=images/stopwatch.png hspace=4><b>'.$text{'timestop'}.'</b></td>';
print			'<td valign="top"><input type="text" name="timestop" size="5" value="'.$timestop.'"></td>';
print			'</tr>';

print 			'<tr><td valign="top"><img src=images/info.png hspace=4><b>'.$text{'description'}.'</b></td>';
print			'<td valign="top"><input type="text" name="description" size="60" value="'.$description.'"></td>';
print			'</tr>';

print			'</table>
			</td>
		</tr>
	</table>';

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
