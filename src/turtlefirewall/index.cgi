#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

&header( $text{'title'}, '', undef, 1 );

print "<br>\n";

@links = ('list_items.cgi','list_nat.cgi','list_rules.cgi','list_services.cgi','edit_options.cgi','log.cgi','backup.cgi');
@titles = ($text{'index_icon_firewall_items'}, $text{'index_icon_nat'}, $text{'index_icon_firewall_rules'},
	$text{'index_icon_firewall_services'}, $text{'index_icon_edit_options'}, $text{'index_icon_log'},
	$text{'index_icon_backup'});
@icons = ('images/items.gif','images/nats.gif','images/rules.gif','images/services.gif',
	'images/options.gif','images/log.gif','images/backup.gif');

icons_table( \@links, \@titles, \@icons );

# $status == 1 if Firewall is ON
$status = $fw->GetStatus();

print '<form action="index.cgi">
	<input name="start" type="submit" value="'.
	( ($status && $in{stop} eq '') || $in{start} ne '' ? $text{'index_restart'} : $text{'index_start'}).'">
	&nbsp;';
	if( ($status && $in{stop} eq '') || $in{start} ne '' ) {
		print '<input name="stop" type="submit" value="'.$text{'index_stop'}.'">&nbsp;';
	}
print '<input name="showiptables" type="submit" value="'.$text{'index_showiptables'}.'">
	<br><br>
	<table width="100%" border="0"><tr>
	<td>
	<i>Turtle Firewall '.$fw->Version().'</i>
	</td>
	<td align="right">
	<i><a href="http://www.turtlefirewall.com" target="_new">www.turtlefirewall.com</a></i>
	</td></tr></table>
	</form>';

if( $in{start} ne '' ) {
	print "<table border width=\"100%\">
		<tr $cb><td>";
	print "<pre><tt>\n";
	print qx{/usr/sbin/turtlefirewall 2>&1};
	print "</tt></pre>";
	print "</td></tr></table>";
}
if( $in{stop} ne '' ) {
	print "<table border width=\"100%\">
		<tr $cb><td>";
	print "<pre><tt>\n";
	print qx{/usr/sbin/turtlefirewall --stop 2>&1};
	print "</tt></pre>";
	print "</td></tr></table>";
}
if( $in{showiptables} ne '' ) {
	print "<br><table border width=\"100%\">
		<tr $tb><th>NAT</th></tr>
		<tr $cb><td>";
	print "<pre><tt><small>";
	print qx{iptables -t nat -L -n -v 2>&1};
	print "</small></tt></pre>";
	print "</td></tr></table>";

	print "<br><table border width=\"100%\">
		<tr $tb><th>MANGLE</th></tr>
		<tr $cb><td>";
	print "<pre><tt><small>";
	print qx{iptables -t mangle -L -n -v 2>&1};
	print "</small></tt></pre>";
	print "</td></tr></table>";

	print "<br><table border width=\"100%\">
		<tr $tb><th>FILTERS</th></tr>
		<tr $cb><td>";
	print "<pre><tt><small>";
	print qx{iptables -L -n -v 2>&1};
	print "</small></tt></pre>";
	print "</td></tr></table>";
}
if( $in{log} ne '' ) {
	print "<table border width=\"100%\">
		<tr $cb><td>";
	#print qx{grep "TFW DROP" $SysLogFile 2>&1};
	showLog();
	print "</td></tr></table>";
}

print "<br>\n";

&footer('/',$text{'index'});


