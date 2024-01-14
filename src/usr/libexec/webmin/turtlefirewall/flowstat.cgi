#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';
use Tie::File;

&ui_print_header( $text{'flowstat_title'}, $text{'title'}, "" );

reportFlowStat();

&ui_print_footer('','turtle firewall index');

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

	my $options_log = '';
	my @logs = glob("${log}*");
	for my $k (@logs) {
		$options_log .= '<option'.($k eq $log ? ' selected' : '').'>'.$k.'</option>';
	}

	my $options_max = '';
	for my $k (@maxs) {
		$options_max .= '<option'.($k eq $max ? ' selected' : '').'>'.$k.'</option>';
	}

	my $options_top = '';
	for my $k (@tops) {
		$options_top .= '<option'.($k eq $top ? ' selected' : '').'>'.$k.'</option>';
	}

	my $options_type = '';
	for my $k (@types) {
		$options_type .= '<option'.($k eq $type ? ' selected' : '').'>'.$k.'</option>';
	}

	$td = "width=20% style='white-space: nowrap;'";
	print &ui_form_start("report_flowstat.cgi", "post");
	print qq~<table border width=\"100%\">
		<tr $tb>
			<th>$text{'edit_flowstat_title_create'}</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\">
			<tr>
				<td $td><b>$text{'edit_flowstat_log'}</b></td>
				<td><select name="log">$options_log</select></td>
			</tr>
			<tr>
				<td $td><b>$text{'edit_flowstat_type'}</b></td>
				<td><select name="type">$options_type</select></td>
			</tr>
	  		<tr>
				<td $td><b>$text{'edit_flowstat_max'}</b></td>
				<td><select name="max">$options_max</select> <small><i>$text{flowstat_max_help}</i></small></td>
			</tr>
			<tr>
				<td $td><b>$text{'edit_flowstat_top'}</b></td>
				<td><select name="top">$options_top</select></td>
			</tr>
			<tr>
				<td><b>$text{'edit_flowstat_string'}</b></td>
				<td><input type="text" size="60" name="string" value="$string"></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>~;

	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_submit( $text{'button_create'}, "create").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
