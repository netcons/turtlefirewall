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

&ui_print_header( $text{'report_flowblacklist_title'}, $text{'title'}, "" );

my $log = $in{'log'};
my $type = $in{'type'};

my $index = $blacklists{$type}{INDEX};
my $blacklist_file = $blacklists{$type}{LOCATION};
 
my @flows = getflows($log);

my %blacklist = getblacklist($blacklist_file);

my @suspect_flows = getsuspect_flows($index,@flows);

showsuspect_flows($type,$index,@suspect_flows);

&ui_print_footer("flowstat.cgi",'flow statistics');

#============================================================================

sub getflows {

	my $log = shift;

	my @log_lines = ();

	use Fcntl 'O_RDONLY';
	tie @log_lines, 'Tie::File', $log, mode => O_RDONLY;

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
		my $ja3s = '';
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
		if( $l =~ /S=(.*?)( |$)/ ) { $ja3s = $1; }
		if( $l =~ /C=(.*?)( |$)/ ) { $ja3c = $1; }
		if( $l =~ /F=(.*?)( |$)/ ) { $tlsfp = $1; }
		if( $l =~ /V=(.*?)( |$)/ ) { $tlsv = $1; }
		if( $l =~ /R=(.*?)( |$)/ ) { $risk = $1; }

		if( $ja3c ne '' || $tlsfp ne '' ) {
			push(@flows, [$stime, $etime, $l3proto, $l4proto, $source, $sport, $destination, $dport,
		      			$ubytes, $dbytes, $upackets, $dpackets, $ifindex,
			       		$connmark, $srcnat, $dstnat, $protocol, $hostname,
					$ja3s, $ja3c, $tlsfp, $tlsv, $risk]);
		}
	}

	untie @log_lines;

	return @flows;
}

sub getblacklist {

	my $blacklist_file = shift;

	my @blacklist_lines = ();

	use Fcntl 'O_RDONLY';
	tie @blacklist_lines, 'Tie::File', $blacklist_file, mode => O_RDONLY;
	my %blacklist = ();

	foreach my $l (@blacklist_lines) {

		my $item = '';
		my $desc = '';

		if( $l =~ /^(.*?),(.*?)$/ ) {
			$item = $1;
			$desc = $2;
		}

		$blacklist{$item} = $desc;
	}

	untie @blacklist_lines;

	return %blacklist;
}

sub getsuspect_flows {

	my $index = shift;
	my @flows = @_;

	my @suspect_flows = ();

	foreach my $f (@flows) {
	       	my $k = $f->[$index];
	       	if( exists $blacklist{$k} ) {
		       push(@suspect_flows, $f);
	       }
       }

	return @suspect_flows;
}


sub showsuspect_flows {

	my $type = shift;
	my $index = shift;
	my @suspect_flows = @_;

	my $blacklistcount = qx{wc -l < $blacklist_file 2>/dev/null};
	if( $blacklistcount eq '' ) { $blacklistcount = '0'; }
	my $logflowcount = qx{wc -l < $log 2>/dev/null};
	my $flowcount = @suspect_flows;

	print "Using blacklist $blacklist_file ( $blacklistcount )";
	print "<br><br>";
	print "Found $flowcount $type blacklisted flows of $logflowcount in $log";
	# Time of first flow
	print " ( ";
	print localtime($suspect_flows[0][0])->strftime('%b %d %X');
	# Time of last flow
	print " --> ";
	print localtime($suspect_flows[$#suspect_flows][1])->strftime('%b %d %X');
	print " )";

	@tds = ( "", "", "", "", "", "" );

	print &ui_columns_start([  "<b>DESCRIPTION</b>", "<b>srcADDR</b>", "<b>dstADDR</b>", "<b>dstPORT</b>", "<b>totalBYTES</b>" ], 100, 0, \@tds);

	foreach my $l (@suspect_flows) {
		local @cols;
		my ($stime, $etime, $l3proto, $l4proto, $src, $sport, $dst, $dport, $ubytes, $dbytes, $upackets, $dpackets, $ifindex,
		    $connmark, $srcnat, $dstnat, $proto, $host, $ja3s, $ja3c, $tlsfp, $tlsv, $risk) = @$l;

		push(@cols, $blacklist{$l->[$index]});

		push(@cols, $src);

		push(@cols, $dst);

		push(@cols, $dport);

		push(@cols, roundbytes($ubytes + $dbytes));

	        print &ui_columns_row(\@cols, \@tds);
	}

	print &ui_columns_end();
}
