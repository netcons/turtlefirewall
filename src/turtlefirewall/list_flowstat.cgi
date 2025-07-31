#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();
use Tie::File;
use Time::Piece;

my $log = $in{'log'};
if( $log =~ /\*/ ) { $log = join("\0", glob("${FlowLogFile}-*")); }
$log =~ s/\0/ UNION ALL select * from /g;
$log = "(select * from $log)";
my $type = $in{'type'};
my $top = $in{'top'};
my $is_target = $in{'is_target'};
my $target_type = $in{'target_type'};
my $target = $in{'target'};
if( $is_target ) {
	if( $target_type eq $type ) { &error( $text{list_flowstat_error1} ); }
	if( $target eq '' ) { &error( $text{list_flowstat_error2} ); }
}
&ui_print_header( "$icons{FLOWSTAT}{IMAGE}$text{'report_flowstat_title'}", $text{'title'}, "" );

if( $type eq 'risk' ) { &LoadNdpiRisks($fw); }

my $logflowtotal = 0;
my $flowtotal = 0;
my $logflowcount = 0;
my $flowcount = 0;

my $firstflowtime = '';
my $lastflowtime = '';

my $query = '';

$query = "select count(*) from $log";
$logflowcount = qx{q -Hp "$query" 2>/dev/null};
$logflowcount =~ s/\n//;

$query = "select sum(ubytes+dbytes) from $log";
$logflowtotal = qx{q -Hp "$query" 2>/dev/null};
$logflowtotal =~ s/\n//;

if( $is_target ) {
	$query = "select sum(ubytes+dbytes) from $log where $target_type = '$target'";
	$flowtotal = qx{q -Hp "$query" 2>/dev/null};
	$flowtotal =~ s/\n//;

	$query = "select count(*) from $log where $target_type = '$target'";
	$flowcount = qx{q -Hp "$query" 2>/dev/null};
	$flowcount =~ s/\n//;

	$query = "select stime from $log where $target_type = '$target' order by stime asc limit 1";
	$firstflowtime = qx{q -Hp "$query" 2>/dev/null};

	$query = "select etime from $log where $target_type = '$target' order by etime desc limit 1";
	$lastflowtime = qx{q -Hp "$query" 2>/dev/null};
} else {
	$flowtotal = $logflowtotal;
	$flowcount = $logflowcount;

	$query = "select stime from $log order by stime asc limit 1";
	$firstflowtime = qx{q -Hp "$query" 2>/dev/null};

	$query = "select etime from $log order by etime desc limit 1";
	$lastflowtime = qx{q -Hp "$query" 2>/dev/null};
}

$firstflowtime =~ s/\n//;
$firstflowtime = localtime($firstflowtime)->strftime('%b %d %X');

$lastflowtime =~ s/\n//;
$lastflowtime = localtime($lastflowtime)->strftime('%b %d %X');

my @stats = &getstats($log,$type,$top,$is_target,$target_type,$target);
my $txtindex = $flowreports{$type}{TXTIDX};
my $icoindex = $flowreports{$type}{ICOIDX};

&showstats($type,$is_target,$target_type,$target,$flowcount,$flowtotal,$logflowcount,$firstflowtime,$lastflowtime,$txtindex,$icoindex,@stats);

&ui_print_footer("edit_flowstat.cgi",'flow statistics');

#============================================================================

sub getstats {

	my $log = shift;
	my $type = shift;
	my $top = shift;
	my $is_target = shift;
	my $target_type = shift;
	my $target = shift;
	my $query = '';

	my @stats = ();

	if( $is_target ) {
		$query = "select $type,sum(ubytes+dbytes) from $log where $type != '' and $target_type = '$target' group by $type order by sum(ubytes+dbytes) desc limit $top";
	} else {
		$query = "select $type,sum(ubytes+dbytes) from $log where $type != '' group by $type order by sum(ubytes+dbytes) desc limit $top";
	}

	foreach my $l (qx{q -Hp "$query" 2>/dev/null}) {
		$l =~ s/\n//;
		my @t = split(/\|/, $l);
		push(@stats, \@t);
	}

	return @stats;
}

sub showstats {

	my $type = shift;
	my $is_target = shift;
	my $target_type = shift;
	my $target = shift;
	my $flowcount = shift;
	my $flowtotal = shift;
	my $logflowcount = shift;
	my $firstflowtime = shift;
	my $lastflowtime = shift;
	my $txtindex = shift;
	my $icoindex = shift;
	my @stats = @_;
	my $graphwidth = 300;

	print "Using $flowcount of $logflowcount flows";
	if( $is_target ) { print " where $target_type is equal to <i>".&ui_text_color($target, 'info')."</i>"; }
	print " ( $firstflowtime --> $lastflowtime )";

	@tds = ( "style=white-space:nowrap", "width=$graphwidth", "", "width=1% style=text-align:right;white-space:nowrap" );

	print &ui_columns_start([ "<b>$text{$txtindex}</b>", "<b>$text{'flowstat_percent'}</b>", "", "<b>$text{'flowstat_traffic'}</b>" ], 100, 0, \@tds);

	foreach my $l (@stats) {
		local @cols;
		my ( $item, $bytes) = @$l;

		# Compared to overall traffic
		my $width = ($bytes/$flowtotal) * $graphwidth;
		my $percent = sprintf("%.1f", ($bytes/$flowtotal) * 100);

		# Compared to type traffic
		#my $width = ($bytes/$stats[0][1]) * $graphwidth;
		#my $percent = sprintf("%.1f", ($bytes/$stats[0][1]) * 100);

		my $graph = sprintf("<img src=images/bar.gif height=5 width=%d>", $width);
		my $greygraph = sprintf("<img src=images/grey-bar.gif height=5 width=%d>", $graphwidth-$width);

		if( $type eq 'risk' ) {
			my @risk_list = ();
			for my $id (split(/,/, $item)) {
				my %risk = $fw->GetNdpiRisk($id);
					push(@risk_list, $risk{'DESCRIPTION'} );
			}
			$item = join(",", @risk_list);
		}

		push(@cols, "$icons{$icoindex}{IMAGE}<i>$item</i>");

		push(@cols, "${graph}${greygraph}");

		push(@cols, "<i>&nbsp;&nbsp;$percent %</i>");

		push(@cols, "<i>".&roundbytes($bytes)."</i>");

	        print &ui_columns_row(\@cols, \@tds);
	}
	print &ui_columns_row([undef, undef, undef, "<b>Total : ".&roundbytes($flowtotal)."</b>"], \@tds);

	print &ui_columns_end();
}
