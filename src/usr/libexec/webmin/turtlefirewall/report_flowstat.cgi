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

&ui_print_header( $text{'report_flowstat_title'}, $text{'title'}, "" );

my $log = $in{'log'};
my $type = $in{'type'};
my $max = $in{'max'};
my $top = $in{'top'};
my $string = $in{'string'};

my $flowtotal = 0;
my %type_list = ();
my @flows = getflows();

my %type_index = ( 'source' => '4', 'destination' => '6', 'protocol' => '16', 'hostname' => '17' );
my @stats = getstats($type_index{$type},\%type_list,\@flows);

$type_name = "flowstat_type_$type";
showstats($type_name,@stats);

&ui_print_footer("flowstat.cgi",'flow statistics');

#============================================================================

sub getflows {

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

		if( $type eq 'source' && $source ne '' ) {$type_list{$source} = '0';}
		if( $type eq 'destination' && $destination ne '' ) {$type_list{$destination} = '0';}
		if( $type eq 'protocol' && $protocol ne '') {$type_list{$protocol} = '0';}
		if( $type eq 'hostname' && $hostname ne '') {$type_list{$hostname} = '0';}

		$flowtotal = ($flowtotal + $ubytes + $dbytes);

		push @flows, [$stime, $etime, $l3proto, $l4proto, $source, $sport, $destination, $dport,
		      		$ubytes, $dbytes, $upackets, $dpackets, $ifindex,
			       	$connmark, $srcnat, $dstnat, $protocol, $hostname];
	}
	return @flows;
}

sub getstats {
	
	my $type_index = shift;
	my ($type_list,$flows) = @_;

	my @stats = ();

	# Sum bytes per Type
	foreach my $f (@{$flows}) { 
		foreach $t (sort keys %{$type_list}) {
			if( $f->[$type_index] eq $t ) { $type_list{$t} = ($type_list{$t} + $f->[8] + $f->[9]); }
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

	print "Using $flowcount of $logflowcount flows from $log";
	if( $string ne '' ) { print " containing <tt>\"$string\"</tt>"; }
	# Time of first flow
	print " ( ";
	print localtime($flows[0][0])->strftime('%b %d %X');
	# Time of last flow
	print " --> ";
	print localtime($flows[$#flows][1])->strftime('%b %d %X');
	print " )";

	@tds = ( "style='white-space: nowrap;'", "width=$graphwidth", "", "" );

	print &ui_columns_start([ "<b>$text{$type_name}</b>", "", "<b>$text{'flowstat_percent'}</b>", "<b>$text{'flowstat_usage'}</b>" ], 100, 0, \@tds);

	foreach my $l (@stats) {
		local @cols;
		my ( $item, $bytes) = @$l;

		# Compared to overall usage
		my $width = ($bytes/$flowtotal) * $graphwidth;
		my $percent = sprintf("%.1f", ($bytes/$flowtotal) * 100);

		# Compared to type usage
		#my $width = ($bytes/$stats[0][1]) * $graphwidth;
		#my $percent = sprintf("%.1f", ($bytes/$stats[0][1]) * 100);

		my $graph = sprintf("<img src=images/bar.gif height=5 width=%d>", $width);

		push(@cols, "<tt>$item</tt>");

		push(@cols, $graph);

		push(@cols, "$percent %");

		push(@cols, "<tt>".roundbytes($bytes)."</tt>");

	        print &ui_columns_row(\@cols, \@tds);
	}
        print &ui_columns_row(["<b>Total</b>", undef, undef, "<tt>".roundbytes($flowtotal)."</tt>"], \@tds);

	print &ui_columns_end();
}
