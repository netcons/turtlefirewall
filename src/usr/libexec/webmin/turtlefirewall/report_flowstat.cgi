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
use Tie::File;
use Time::Piece;

&ui_print_header( "<img src=images/graph.png hspace=4>$text{'report_flowstat_title'}", $text{'title'}, "" );

my $log = $in{'log'};
my $type = $in{'type'};
my $max = $in{'max'};
my $top = $in{'top'};
my $string = $in{'string'};

if( $type eq 'risk' ) { LoadNdpiRisks( $fw ); }

my $flowtotal = 0;
my %type_list = ();
my @flows = getflows($log);

my $index = $flowreports{$type}{INDEX};

my @stats = getstats($index,\%type_list,\@flows);

$type_name = "flowstat_type_${type}";
showstats($type_name,@stats);

&ui_print_footer("flowstat.cgi",'flow statistics');

#============================================================================

sub getflows {

	my $log = shift;

	my @last_log_lines = ();

	use Fcntl 'O_RDONLY';
	tie @log_lines, 'Tie::File', $log, mode => O_RDONLY;
		if( $max ne 'all' ) {
			@last_log_lines = ($max >= @log_lines) ? @log_lines : @log_lines[-$max..-1];
		} else { 
			@last_log_lines = @log_lines;
		}
	untie @log_lines;

	my @log_lines = ();

	if( $string ne '' ) {
		@log_lines = grep(/$string/, @last_log_lines);
	} else {
		@log_lines = @last_log_lines;
	}
	
	my @flows = ();

	foreach my $l (@log_lines) {

		my $stime = '';
		my $etime = '';
		my $l3proto = '';
		my $l4proto = '';
		my $source = '';
		my $sport = '';
		my $destination = '';
		my $dport = '';
		my $ubytes = '';
		my $dbytes = '';
		my $upackets = '';
		my $dpackets = '';
		my $ifindex = '';
		my $connmark = '';
		my $srcnat = '';
		my $dstnat = '';
		my $protocol = '';
		my $hostname = '';
		my $ja4c = '';
		my $ja3c = '';
		my $tlsfp = '';
		my $tlsv = '';
		my $risk = '';

		if( $l =~ /^(.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) (.*?) / ) {
			$stime = $1;
			$etime = $2;
			$l3proto = $3;
			$l4proto = $4;
			$source = $5;
			$sport = $6;
			$destination = $7;
			$dport = $8;
			$ubytes = $9;
			$dbytes = $10;
			$upackets = $11;
			$dpackets = $12;
			$ifindex = $13;
		}

		if( $l =~ /CM=(.*?)( |$)/ ) { $connmark = $1; }
		if( $l =~ /SN=(.*?)( |$)/ ) { $srcnat = $1; }
		if( $l =~ /DN=(.*?)( |$)/ ) { $dstnat = $1; }
		if( $l =~ /P=(.*?)( |$)/ ) { $protocol = $1; }
		if( $l =~ /H=(.*?)( |$)/ ) { $hostname = $1; }
		if( $l =~ /c=(.*?)( |$)/ ) { $ja4c = $1; }
		if( $l =~ /C=(.*?)( |$)/ ) { $ja3c = $1; }
		if( $l =~ /F=(.*?)( |$)/ ) { $tlsfp = $1; }
		if( $l =~ /V=(.*?)( |$)/ ) { $tlsv = $1; }
		if( $l =~ /R=(.*?)( |$)/ ) { $risk = $1; }

		if( $type eq 'source' && $source ne '' ) {$type_list{$source} = '0';}
		if( $type eq 'destination' && $destination ne '' ) {$type_list{$destination} = '0';}
		if( $type eq 'dport' && $dport ne '' ) {$type_list{$dport} = '0';}
		if( $type eq 'protocol' && $protocol ne '') {$type_list{$protocol} = '0';}
		if( $type eq 'hostname' && $hostname ne '') {$type_list{$hostname} = '0';}
		if( $type eq 'risk' && $risk ne '') {$type_list{$risk} = '0';}

		$flowtotal = ($flowtotal + $ubytes + $dbytes);

		push @flows, [$stime, $etime, $l3proto, $l4proto, $source, $sport, $destination, $dport,
		      		$ubytes, $dbytes, $upackets, $dpackets, $ifindex,
			       	$connmark, $srcnat, $dstnat, $protocol, $hostname,
			       	$ja4c, $ja3c, $tlsfp, $tlsv, $risk];
	}
	return @flows;
}

sub getstats {
	
	my $index = shift;
	my ($type_list,$flows) = @_;

	my @stats = ();

	# Sum bytes per Type
	foreach my $f (@{$flows}) { 
		foreach $t (sort keys %{$type_list}) {
			if( $f->[$index] eq $t ) { $type_list{$t} = ($type_list{$t} + $f->[8] + $f->[9]); }
		}
	}

	# Sort Items by bytes
	my $count = 0;
	foreach $t (sort { $type_list{$b} <=> $type_list{$a} } keys %{$type_list}) {
		push(@stats, [$t,$type_list{$t}]);
		$count++;
		last if($count == $top);
	}
	return @stats;
}

sub showstats {

	my $type_name = shift;
	my @stats = @_;
	my $graphwidth = 300;

	my $logflowcount = qx{wc -l < $log 2>/dev/null};
	my $flowcount = @flows;

	my $firstflowtime = localtime($flows[0][0])->strftime('%b %d %X');
	my $lastflowtime = localtime($flows[$#flows][1])->strftime('%b %d %X');

	print "Using $flowcount of $logflowcount flows from $log";
	if( $string ne '' ) { print " containing <i>".&ui_text_color($string, 'info')."</i>"; }
	print " ( $firstflowtime --> $lastflowtime )";

	@tds = ( "style=white-space:nowrap", "width=$graphwidth", "", "width=1% align=right style=white-space:nowrap" );

	print &ui_columns_start([ "<b>$text{$type_name}</b>", "<b>$text{'flowstat_percent'}</b>", "", "<b>$text{'flowstat_traffic'}</b>" ], 100, 0, \@tds);

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

		push(@cols, "<i>$item</i>");

		push(@cols, "${graph}${greygraph}");

		push(@cols, "<i>&nbsp;&nbsp;$percent %</i>");

		push(@cols, "<i>".&roundbytes($bytes)."</i>");

	        print &ui_columns_row(\@cols, \@tds);
	}
	print &ui_columns_row([undef, undef, undef, "<b>Total : ".&roundbytes($flowtotal)."</b>"], \@tds);

	print &ui_columns_end();
}
