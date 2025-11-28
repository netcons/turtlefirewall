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
use Time::Piece;

&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_flowlog'}", $text{'title'}, "" );

&LoadNdpiRisks($fw);
&showLog();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showLog {

	my $pag = $in{pag};
	if( $pag == 0 ) { $pag = 1; }
	my $count = 0;
	my $pagelen = 20;
	my @buffer = ();

	#my %l3proto_list = ('*' => undef);
	#my %l4proto_list = ('* '=> undef);
	my %source_list = ('*' => undef);
	#my %sport_list = ('*' => undef);
	#my %destination_list = ('*' => undef);
	#my %dport_list = ('*' => undef);
	#my %ubytes_list = ('*' => undef);
	#my %dbytes_list = ('*' => undef);
	#my %upackets_list = ('*' => undef);
	#my %dpackets_list = ('*' => undef);
	#my %ifindex_list = ('*' => undef);
	#my %connmark_list = ('*' => undef);
	#my %srcnat_list = ('*' => undef);
	#my %dstnat_list = ('*' => undef);
	#my %protocol_list = ('*' => undef);
	#my %hostname_list = ('*' => undef);
	#my %ja4c_list = ('*' => undef);
	#my %tlsfp_list = ('*' => undef);
	#my %risk_list = ('*' => undef);

	open( LOG, "<", $FlowLogFile );
	while (my $l = <LOG>) {

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
			if( $l =~ /H=(.*?)( |$)/ && $l !~ /H=\"(.*?)\"( |$)/ ) { $hostname = $1; }
			if( $l =~ /c=(.*?)( |$)/ ) { $ja4c = $1; }
			if( $l =~ /F=(.*?)( |$)/ ) { $tlsfp = $1; }
			if( $l =~ /R=(.*?)( |$)/ ) { $risk = $1; }

			#if( $l3proto ne '' ) {$l3proto_list{$l3proto} = undef;}
			#if( $l4proto ne '' ) {$l4proto_list{$l4proto} = undef;}
			if( $source ne '' ) {$source_list{$source} = undef;}
			#if( $sport ne '' ) {$sport_list{$sport} = undef;}
			#if( $destination ne '' ) {$destination_list{$destination} = undef;}
			#if( $dport ne '' ) {$dport_list{$dport} = undef;}
			#if( $ubytes ne '' ) {$ubytes_list{$ubytes} = undef;}
			#if( $dbytes ne '' ) {$dbytes_list{$dbytes} = undef;}
			#if( $upackets ne '' ) {$upackets_list{$upackets} = undef;}
			#if( $dpackets ne '' ) {$dpackets_list{$dpackets} = undef;}
			#if( $ifindex ne '' ) {$ifindex_list{$ifindex} = undef;}
			#if( $connmark ne '' ) {$connmark_list{$connmark} = undef;}
			#if( $srcnat ne '' ) {$srcnat_list{$srcnat} = undef;}
			#if( $dstnat ne '' ) {$dstnat_list{$dstnat} = undef;}
			#if( $protocol ne '') {$protocol_list{$protocol} = undef;}
			#if( $hostname ne '') {$hostname_list{$hostname} = undef;}
			#if( $ja4c ne '') {$ja4c_list{$ja4c} = undef;}
			#if( $tlsfp ne '') {$tlsfp_list{$tlsfp} = undef;}
			#if( $risk ne '') {$risk_list{$risk} = undef;}

			if( ($in{l3proto} eq '' || $in{l3proto} eq '*' || $in{l3proto} eq $l3proto) &&
			    ($in{l4proto} eq '' || $in{l4proto} eq '*' || $in{l4proto} eq $l4proto) &&
			    ($in{source} eq '' || $in{source} eq '*' || $in{source} eq $source) &&
			    ($in{sport} eq '' || $in{sport} eq '*' || $in{sport} eq $sport) &&
			    ($in{destination} eq '' || $in{destination} eq '*' || $in{destination} eq $destination) &&
			    ($in{dport} eq '' || $in{dport} eq '*' || $in{dport} eq $dport) &&
			    ($in{ubytes} eq '' || $in{ubytes} eq '*' || $in{ubytes} eq $ubytes) &&
			    ($in{dbytes} eq '' || $in{dbytes} eq '*' || $in{dbytes} eq $dbytes) &&
			    ($in{upackets} eq '' || $in{upackets} eq '*' || $in{upackets} eq $upackets) &&
			    ($in{dpackets} eq '' || $in{dpackets} eq '*' || $in{dpackets} eq $dpackets) &&
			    ($in{ifindex} eq '' || $in{ifindex} eq '*' || $in{ifindex} eq $ifindex) &&
			    ($in{connmark} eq '' || $in{connmark} eq '*' || $in{connmark} eq $connmark) &&
			    ($in{srcnat} eq '' || $in{srcnat} eq '*' || $in{srcnat} eq $srcnat) &&
			    ($in{dstnat} eq '' || $in{dstnat} eq '*' || $in{dstnat} eq $dstnat) &&
			    ($in{protocol} eq '' || $in{protocol} eq '*' || $in{protocol} eq $protocol) &&
			    ($in{hostname} eq '' || $in{hostname} eq '*' || $in{hostname} eq $hostname) &&
			    ($in{ja4c} eq '' || $in{ja4c} eq '*' || $in{ja4c} eq $ja4c) &&
			    ($in{tlsfp} eq '' || $in{tlsfp} eq '*' || $in{tlsfp} eq $tlsfp) &&
			    ($in{risk} eq '' || $in{risk} eq '*' || $in{risk} eq $risk) ) {
				$count++;

				if( $count >= ($pag-1) * $pagelen && $count < $pag * $pagelen) {
					push @buffer, [$stime, $etime, $l3proto, $l4proto, $source, $sport, $destination, $dport,
					      		$ubytes, $dbytes, $upackets, $dpackets, $ifindex,
						       	$connmark, $srcnat, $dstnat, $protocol, $hostname,
						       	$ja4c, $tlsfp, $risk];
				}
			}
	}
	close( LOG );

	# Pages index
	my $urlparam = 'stime='.$in{stime}.'&etime='.$in{etime}.'&l3proto='.$in{l3proto}.'&l4proto='.$in{l4proto}.
			'&source='.$in{source}.'&sport='.$in{sport}.'&destination='.$in{destination}.'&dport='.$in{dport}.'&ubytes='.$in{ubytes}.'&dbytes='.$in{dbytes}.
			'&upackets='.$in{upackets}.'&dpackets='.$in{dpackets}.'&ifindex='.$in{ifindex}.
			'&connmark='.$in{connmark}.'&srcnat='.$in{srcnat}.'&dstnat='.$in{dstnat}.
			'&protocol='.$in{protocol}.'&hostname='.$in{hostname}.'&ja4c='.$in{ja4c}.
			'&tlsfp='.$in{tlsfp}.'&risk='.$in{risk};
	my $pageindex = '';
	if( $pag > 1 ) {
		$pageindex .= "&nbsp;<a href=\"list_flowlog.cgi?pag=1&$urlparam\">&lt;&lt;</a>&nbsp;";
		$pageindex .= "&nbsp;<a href=\"list_flowlog.cgi?pag=".($pag-1)."&$urlparam\">&lt;</a>&nbsp;";
	}
	$pageindex .= "&nbsp;(<b>$pag</b>)&nbsp;";
	$lastpag = int(($count-1) / $pagelen) + 1;
	if( $pag < $lastpag ) {
		$pageindex .= "&nbsp;<a href=\"list_flowlog.cgi?pag=".($pag+1)."&$urlparam\">&gt;</a>&nbsp;";
		$pageindex .= qq~&nbsp;<a href="list_flowlog.cgi?pag=$lastpag&$urlparam">&gt;&gt;</a>&nbsp;~;
	}

	print &ui_form_start("list_flowlog.cgi", "post");
	print "<div style=text-align:center>$pageindex</div>\n";

	my $opz;

	local @head;

	local $hstime;
	$hstime .= "<b>startTIME<br></b>";
	push(@head, $hstime );

	local $hetime;
	$hetime .= "<b>endTIME<br></b>";
	push(@head, $hetime );

	local $hl3proto;
	$hl3proto .= "<b>L3PROTO<br></b>";
	push(@head, $hl3proto );

	local $hl4proto;
	$hl4proto .= "<b>L4PROTO<br></b>";
	push(@head, $hl4proto );

	local $hprotocol;
	$hprotocol .= "<b>L7PROTO<br></b>";
	push(@head, $hprotocol );

	local $hhostname;
	$hhostname .= "<b>hostNAME<br></b>";
	push(@head, $hhostname );

	local $hsource;
	$hsource .= "<b>srcADDR<br><select name='source' size='1'>";
	foreach $opz (sort keys %source_list) {$hsource .= "<option".($in{source} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hsource .= "</select></b>";
	push(@head, $hsource );

	local $hsport;
	$hsport .= "<b>srcPORT<br></b>";
	push(@head, $hsport );

	local $hdestination;
	$hdestination .= "<b>dstADDR<br></b>";
	push(@head, $hdestination );

	local $hdport;
	$hdport .= "<b>dstPORT<br></b>";
	push(@head, $hdport );

	local $htbytes;
	$htbytes .= "<b>totalBYTES<br></b>";
	push(@head, $htbytes );

	local $hubytes;
	$hubytes .= "<b>upBYTES<br></b>";
	push(@head, $hubytes );

	local $hdbytes;
	$hdbytes .= "<b>downBYTES<br></b>";
	push(@head, $hdbytes );

	local $hupackets;
	$hupackets .= "<b>upPACKETS<br></b>";
	push(@head, $hupackets );

	local $hdpackets;
	$hdpackets .= "<b>downPACKETS<br></b>";
	push(@head, $hdpackets );

	local $hinif;
	$hinif .= "<b>inIF<br></b>";
	push(@head, $hinif );

	local $houtif;
	$houtif .= "<b>outIF<br></b>";
	push(@head, $houtif );

	local $hconnmark;
	$hconnmark .= "<b>connMARK<br></b>";
	push(@head, $hconnmark );

	local $hsrcnat;
	$hsrcnat .= "<b>srcNAT<br></b>";
	push(@head, $hsrcnat );

	local $hdstnat;
	$hdstnat .= "<b>dstNAT<br></b>";
	push(@head, $hdstnat );

	local $hja4c;
	$hja4c .= "<b>ja4cFINGERPRINT<br></b>";
	push(@head, $hja4c );

	local $htlsfp;
	$htlsfp .= "<b>tlsFINGERPRINT<br></b>";
	push(@head, $htlsfp );

	local $hrisk;
	$hrisk .= "<b>RISK<br></b>";
	push(@head, $hrisk );

	@tds = ( "style=white-space:nowrap",
	       	 "style=white-space:nowrap",
		 "style=text-align:center",
		 "style=text-align:center",
		 "style=white-space:nowrap",
		 "style=white-space:nowrap",
		 "style=white-space:nowrap",
		 "",
		 "style=white-space:nowrap",
		 "",
		 "",
		 "",
		 "",
		 "style=text-align:center",
		 "style=text-align:center",
		 "",
		 "",
		 "",
		 "style=white-space:nowrap",
		 "style=white-space:nowrap",
		 "style=white-space:nowrap",
		 "style=white-space:nowrap",
		 "style=white-space:nowrap" );
	print &ui_columns_start(\@head, 100, 0, \@tds);

	foreach my $l (@buffer) {
		local @cols;
		my ($stime, $etime, $l3proto, $l4proto, $source, $sport, $destination, $dport, $ubytes, $dbytes, $upackets, $dpackets, $ifindex,
		    $connmark, $srcnat, $dstnat, $protocol, $hostname, $ja4c, $tlsfp, $risk) = @$l;
	    	&showTD(localtime($stime)->strftime('%b %d %X'));
	    	&showTD(localtime($etime)->strftime('%b %d %X'));
		&showTD(&l3protoname($l3proto));
		&showTD(&l4protoname($l4proto));
		&showTD($protocol);
		&showTD($hostname);
		&showTD($source);
		&showTD($sport);
		&showTD($destination);
		&showTD($dport);
		&showTD(&roundbytes($ubytes + $dbytes));
		&showTD(&roundbytes($ubytes));
		&showTD(&roundbytes($dbytes));
		&showTD($upackets);
		&showTD($dpackets);
		$t = $ifindex;
		if( $t =~ /I=(.*?)(,|$)/ ) { $inifindex = $1; };
		&showTD(&getifname($inifindex));
		if( $t =~ /,(.*?)$/ ) { $outifindex = $1; };
		&showTD(&getifname($outifindex));
		&showTD($connmark);
		&showTD($srcnat);
		&showTD($dstnat);
		&showTD($ja4c);
		&showTD($tlsfp);
		&showTD(&getrisknames($risk));
	        print &ui_columns_row(\@cols, \@tds);
	}
	print &ui_columns_end();

	print "<table width=100%><tr>";
	print '<td style=text-align:right>'.&ui_submit( $text{'log_update'} ).'</td>';
	print "</tr></table>";

	print &ui_form_end();

	print "<div style=text-align:center>$pageindex</div>\n";
}

sub showTD {
	my $text = shift;

	if( $text eq '' ) { $text = '&nbsp;'; }
	push(@cols, "<i>$text&nbsp;&nbsp;</i>");
}

sub l3protoname {
	my $num = shift;
	my $protoname = '';

	if( $num eq '4' ) { $protoname = 'ipv4'; }
	if( $num eq '6' ) { $protoname = 'ipv6'; }
	return $protoname;
}

sub l4protoname {
	my $num = shift;
	my $protoname = '';

	if( $num eq '1' ) { $protoname = 'icmp'; }
	if( $num eq '6' ) { $protoname = 'tcp'; }
	if( $num eq '17' ) { $protoname = 'udp'; }
	return $protoname;
}

sub getifname {
	my $index = shift;
	my $ifname = '';

	if ( $index eq '0' || $index eq '' ) {
		$ifname = 'none';
	} else {
		$cmd_output = qx(ip link show | grep "^$index:");
		if( $cmd_output =~ /(.*?) (.*?)(@|:)/ ) { $ifname = $2 } else { $ifname = 'unknown' };
	}
	return $ifname;
}
sub getrisknames {
	my $risks = shift;
	my $risknames = '';

	my @items = ();

	for my $id (split(/,/, $risks)) {
		my %risk = $fw->GetNdpiRisk($id);
		push(@items, $risk{'DESCRIPTION'} );
	}
	$risknames = join(",", @items);
	return $risknames;
}
