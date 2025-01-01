#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';
use Tie::File;

&ui_print_header( "$icons{CREATE}{IMAGE}$text{'edit_flowstat_title_create'}", $text{'title'}, "" );

&reportFlowStat();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub reportFlowStat {

	my $log = $FlowLogFile;

	my @types = sort keys %flowreports;
	my @maxs = ( 'all', '100', '1000', '10000', '100000' );
	my @tops = ( '5', '10', '15', '20' );

	#my $type = $types[0];
	my $type = 'protocol';
	my $max = $maxs[1];
	my $top = $tops[0];
	my $string = '';

	my @logs = glob("${log}*");

	print &ui_subheading("$icons{CREATE}{IMAGE}$text{'edit_flowstat_title_create'}");
	print &ui_form_start("list_flowstat.cgi", "post");
	my @tds = ( "width=20% style=white-space:nowrap ", "width=80%" );
	print &ui_columns_start(undef, 100, 0, \@tds);
	my $col = '';
	$col = &ui_select("log", $log, \@logs);
	print &ui_columns_row([ "$icons{LOG}{IMAGE}<b>$text{'edit_flowstat_log'}</b>", $col ], \@tds);
	$col = &ui_select("type", $type, \@types);
	print &ui_columns_row([ "$icons{OPTION}{IMAGE}<b>$text{'edit_flowstat_type'}</b>", $col ], \@tds);
	$col = &ui_select("max", $max, \@maxs);
	$col .= "<small><i>$text{flowstat_max_help}</i></small>";
	print &ui_columns_row([ "$icons{RATELIMIT}{IMAGE}<b>$text{'edit_flowstat_max'}</b>", $col ], \@tds);
	$col = &ui_select("top", $top, \@tops);
	print &ui_columns_row([ "$icons{FLOWSTAT}{IMAGE}<b>$text{'edit_flowstat_top'}</b>", $col ], \@tds);
	$col = &ui_textbox("string", $string, 60, 0, 60);
	print &ui_columns_row([ "$icons{TARGET}{IMAGE}<b>$text{'edit_flowstat_string'}</b>", $col ], \@tds);
	print &ui_columns_end();

	print "<table width=100%><tr>";
	print '<td>'.&ui_submit( $text{'button_create'}, "create").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
