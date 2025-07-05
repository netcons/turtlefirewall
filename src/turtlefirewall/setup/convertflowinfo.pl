#!/usr/bin/env perl

# Turtle Firewall : Convert Flow Info
#
# Software for configuring a linux firewall (netfilter)
#
#   2001/11/23 13:25:00
#
#======================================================================
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

use Tie::File;

my $log;

foreach my $arg (@ARGV) {
	if( $arg =~ /^(--log)\=(.*)/ ) {
		$log = $2;
	} else {
		if( $arg ne '--help' ) {
			print "Wrong parameters...\n";
		}
		print "Use: convertflowinfo.pl [--log=file] [--help]\n";
		print "Example: convertflowinfo.pl --log=/tmp/flowinfo.log\n";
		exit(1);
	}
}

if( $log eq '' ) { print "Error: no log provided\n"; exit(1); }
if( ! -f $log ) { print "Error: $log not found\n"; exit(1); }

&convert2psv($log);

# Create sqlite
system("q -C readwrite -Hp 'select * from $log' > /dev/null 2>&1");

system("mv -f ${log}.qsql $log");

#============================================================================

sub convert2psv {

	my $log = shift;

	tie @log_lines, 'Tie::File', $log;

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
		my $tlsfp = '';
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
		if( $l =~ /F=(.*?)( |$)/ ) { $tlsfp = $1; }
		if( $l =~ /R=(.*?)( |$)/ ) { $risk = $1; }

		$l = "$stime|$etime|$l3proto|$l4proto|$source|$sport|$destination|$dport|$ubytes|$dbytes|$upackets|$dpackets|$ifindex|$connmark|$srcnat|$dstnat|$protocol|$hostname|$ja4c|$tlsfp|$risk\n";
	}
	my $psvheader = 'stime|etime|l3proto|l4proto|source|sport|destination|dport|ubytes|dbytes|upackets|dpackets|ifindex|connmark|srcnat|dstnat|protocol|hostname|ja4c|tlsfp|risk';
	unshift @log_lines, $psvheader;

	untie @log_lines;
}
