#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
use Tie::File;

&ui_print_header( "$icons{CREATE}{IMAGE}$text{'edit_flowstat_title_create'}", $text{'title'}, "" );

&reportFlowStat();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub reportFlowStat {

	my @types = sort keys %flowreports;
	my @tops = ( '5', '10', '25', '50' );

	my $log = '';
	my $type = 'protocol';
	my $top = '5';
	my $is_target = 0;
	my $target_type = 'source';
	my $target = '';

	my @logs = ('*');
	push @logs, sort { $b cmp $a } glob("${FlowLogFile}-*");
	my $selected_log = $logs[1];

	print &ui_subheading("$icons{CREATE}{IMAGE}$text{'edit_flowstat_title_create'}");
	print &ui_form_start("list_flowstat.cgi", "post");
	my @tds = ( "width=20% style=white-space:nowrap", "width=80%" );
	print &ui_columns_start(undef, 100, 0, \@tds);
	my $col = '';
	$col = &ui_select("log", $selected_log, \@logs, 5, 1);
	print &ui_columns_row([ "$icons{LOG}{IMAGE}<b>$text{'edit_flowstat_log'}</b>", $col ], \@tds);
	$col = &ui_select("type", $type, \@types);
	print &ui_columns_row([ "$icons{OPTION}{IMAGE}<b>$text{'edit_flowstat_type'}</b>", $col ], \@tds);
	$col = &ui_select("top", $top, \@tops);
	print &ui_columns_row([ "$icons{FLOWSTAT}{IMAGE}<b>$text{'edit_flowstat_top'}</b>", $col ], \@tds);

	my @opts = ( [ 0, "$text{NO}<br>" ], [ 1, "$text{YES}" ] );
	$col = &ui_radio("is_target", $is_target ? 1 : 0, \@opts);
	$col .= "&nbsp; where &nbsp;";
	$col .= &ui_select("target_type", $target_type, \@types);
	$col .= "&nbsp; is equal to &nbsp;";
	$col .= &ui_textbox("target", $target, 60, 0, 60);
	print &ui_columns_row([ "$icons{TARGET}{IMAGE}<b>$text{'edit_flowstat_target'}</b>", $col ], \@tds);

	print &ui_columns_end();

	print "<table width=100%><tr>";
	print '<td>'.&ui_submit( $text{'button_create'}, "create").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
