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

&ui_print_header( "$icons{ICON}{IMAGE} v ".$fw->Version(), $text{'title'}, "", undef, 1, 1, 0,
        &help_search_link("iptables", "man", "doc"));

my @olinks = ('list_items.cgi',
	     'list_services.cgi',
	     'list_ndpiprotocols.cgi',
	     'list_ndpirisks.cgi',
	     'list_countrycodes.cgi',
	     'edit_options.cgi',
	     'backup.cgi');
my @otitles = ($text{'index_icon_items'},
	      $text{'index_icon_services'},
	      $text{'index_icon_ndpiprotocols'},
	      $text{'index_icon_ndpirisks'},
	      $text{'index_icon_countrycodes'},
              $text{'index_icon_options'},
              $text{'index_icon_backup'});
my @oicons = ('images/items.png',
	     'images/services.png',
	     'images/ndpiprotocols.png',
	     'images/ndpirisks.png',
	     'images/countrycodes.png',
	     'images/options.png',
	     'images/backup.png');
&icons_table(\@olinks, \@otitles, \@oicons, 10);
print &ui_hr();

my @rlinks = ('list_rules.cgi',
	      'list_nat.cgi',
	      'list_manglerules.cgi',
	      'list_rawrules.cgi');
my @rtitles = ($text{'index_icon_rules'},
               $text{'index_icon_nat'},
               $text{'index_icon_manglerules'},
               $text{'index_icon_rawrules'});
my @ricons = ('images/rules.png',
	      'images/nats.png',
	      'images/manglerules.png',
	      'images/rawrules.png');
&icons_table(\@rlinks, \@rtitles, \@ricons, 4);
print &ui_hr();

my @llinks = ('list_actionlog.cgi',
	      'list_flowlog.cgi',
	      'edit_flowstat.cgi');
my @ltitles = ($text{'index_icon_log'},
	       $text{'index_icon_flowlog'},
               $text{'index_icon_flowstat'});
my @licons = ('images/log.png',
 	      'images/flowlog.png',
	      'images/flowstat.png');
&icons_table(\@llinks, \@ltitles, \@licons, 3);
print &ui_hr();

# $status == 1 if Firewall is ON
$status = $fw->GetStatus();

print '<table width=100%><tr>';
print '<td>';
print &ui_form_start("start.cgi", "post");
if ( ($status && $in{stop} eq '') || $in{start} ne '') {
	print &ui_submit( $text{'index_restart'}, "restart");
} else {
	print &ui_submit( $text{'index_start'}, "start");
}	
print &ui_form_end();
print '</td>';
print '<td style=text-align:right>';
print &ui_form_start("stop.cgi", "post");
if( ($status && $in{stop} eq '') || $in{start} ne '' ) {
	print &ui_submit( $text{'index_stop'}, "stop");
}
print &ui_form_end();
print '</td>';
print '</tr></table>';

print &ui_hr();

print &ui_form_start("index.cgi", "post");
print '<table width="100%"><tr>';
print '<td>';
print &ui_submit( $text{'index_showiptfilter'}, "showiptfilter");
print &ui_submit( $text{'index_showiptnat'}, "showiptnat");
print &ui_submit( $text{'index_showiptmangle'}, "showiptmangle");
print &ui_submit( $text{'index_showiptraw'}, "showiptraw");
print '</td>';
print '<td style=text-align:right>';
print &ui_submit( $text{'index_showconntrack'}, "showconntrack");
print &ui_submit( $text{'index_flushconntrack'}, "flushconntrack");
print '</td>';
print '</tr></table>';
print &ui_form_end();

if( $in{showiptfilter} ne '' ) {
	print "<br><table border=0 width=100%>
		<tr $tb><th>FILTER</th></tr>
		<tr $cb><td>";
	print "<pre><small>";
	print qx{iptables -L -n -v -x 2>&1};
	#print qx{nft list table ip filter 2>&1};
	print "</small></pre>";
	print "</td></tr></table>";
}

if( $in{showiptnat} ne '' ) {
	print "<br><table border=0 width=100%>
		<tr $tb><th>NAT</th></tr>
		<tr $cb><td>";
	print "<pre><small>";
	print qx{iptables -t nat -L -n -v -x 2>&1};
	#print qx{nft list table ip nat 2>&1};
	print "</small></pre>";
	print "</td></tr></table>";
}

if( $in{showiptmangle} ne '' ) {
	print "<br><table border=0 width=100%>
		<tr $tb><th>MANGLE</th></tr>
		<tr $cb><td>";
	print "<pre><small>";
	print qx{iptables -t mangle -L -n -v -x 2>&1};
	#print qx{nft list table ip mangle 2>&1};
	print "</small></pre>";
	print "</td></tr></table>";
}

if( $in{showiptraw} ne '' ) {
	print "<br><table border=0 width=100%>
		<tr $tb><th>RAW</th></tr>
		<tr $cb><td>";
	print "<pre><small>";
	print qx{iptables -t raw -L -n -v -x 2>&1};
	#print qx{nft list table ip raw 2>&1};
	print "</small></pre>";
	print "</td></tr></table>";
}

if( $in{showconntrack} ne '' ) {
	print "<br><table border=0 width=100%>
		<tr $tb><th>CONNTRACK</th></tr>
		<tr $cb><td>";
	print "<pre><small>";
	print qx{/usr/sbin/conntrack -L -o extended};
	print "</small></pre>";
	print "</td></tr></table>";
}

if( $in{flushconntrack} ne '' ) {
	print "<br><table border=0 width=100%>
		<tr $tb><th>CONNTRACK</th></tr>
		<tr $cb><td>";
	print "<pre><small>";
	print qx{/usr/sbin/conntrack -F 2>&1};
	print "</small></pre>";
	print "</td></tr></table>";
}

print "<br>\n";

&ui_print_footer("/", $text{'index'});
