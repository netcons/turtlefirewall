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
use Time::Piece;

&ui_print_header( "<img src=images/grey-eye.png hspace=4>$text{'flowlog_title'}", $text{'title'}, "" );

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

	#my %l3proto_list = ('*'=>'x');
	#my %l4proto_list = ('*'=>'x');
	my %src_list = ('*' => undef);
	#my %sport_list = ('*'=>'x');
	#my %dst_list = ('*'=>'x');
	#my %dport_list = ('*'=>'x');
	#my %ubytes_list = ('*'=>'x');
	#my %dbytes_list = ('*'=>'x');
	#my %upackets_list = ('*'=>'x');
	#my %dpackets_list = ('*'=>'x');
	#my %ifindex_list = ('*'=>'x');
	#my %connmark_list = ('*'=>'x');
	#my %srcnat_list = ('*'=>'x');
	#my %dstnat_list = ('*'=>'x');
	#my %proto_list = ('*'=>'x');
	#my %host_list = ('*'=>'x');
	#my %ja4c_list = ('*'=>'x');
	#my %ja3c_list = ('*'=>'x');
	#my %tlsfp_list = ('*'=>'x');
	#my %tlsv_list = ('*'=>'x');
	#my %risk_list = ('*'=>'x');

	open( LOG, "<", $FlowLogFile );
	while( <LOG> ) {
			my $l = $_;

			my $stime = '';
			my $etime = '';
			my $l3proto = '';
			my $l4proto = '';
			my $src = '';
			my $sport = '';
			my $dst = '';
			my $dport = '';
			my $ubytes = '';
			my $dbytes = '';
			my $upackets = '';
			my $dpackets = '';
			my $ifindex = '';
			my $connmark = '';
			my $srcnat = '';
			my $dstnat = '';
			my $proto = '';
			my $host = '';
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
				$src = $5;
				$sport = $6;
				$dst = $7;
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
			if( $l =~ /P=(.*?)( |$)/ ) { $proto = $1; }
			if( $l =~ /H=(.*?)( |$)/ ) { $host = $1; }
			if( $l =~ /c=(.*?)( |$)/ ) { $ja4c = $1; }
			if( $l =~ /C=(.*?)( |$)/ ) { $ja3c = $1; }
			if( $l =~ /F=(.*?)( |$)/ ) { $tlsfp = $1; }
			if( $l =~ /V=(.*?)( |$)/ ) { $tlsv = $1; }
			if( $l =~ /R=(.*?)( |$)/ ) { $risk = $1; }

			#if( $l3proto ne '' ) {$l3proto_list{$l3proto} = 'x';}
			#if( $l4proto ne '' ) {$l4proto_list{$l4proto} = 'x';}
			if( $src ne '' ) {$src_list{$src} = undef;}
			#if( $sport ne '' ) {$sport_list{$sport} = 'x';}
			#if( $dst ne '' ) {$dst_list{$dst} = 'x';}
			#if( $dport ne '' ) {$dport_list{$dport} = 'x';}
			#if( $ubytes ne '' ) {$ubytes_list{$ubytes} = 'x';}
			#if( $dbytes ne '' ) {$dbytes_list{$dbytes} = 'x';}
			#if( $upackets ne '' ) {$upackets_list{$upackets} = 'x';}
			#if( $dpackets ne '' ) {$dpackets_list{$dpackets} = 'x';}
			#if( $ifindex ne '' ) {$ifindex_list{$ifindex} = 'x';}
			#if( $connmark ne '' ) {$connmark_list{$connmark} = 'x';}
			#if( $srcnat ne '' ) {$srcnat_list{$srcnat} = 'x';}
			#if( $dstnat ne '' ) {$dstnat_list{$dstnat} = 'x';}
			#if( $proto ne '') {$proto_list{$proto} = 'x';}
			#if( $host ne '') {$host_list{$host} = 'x';}
			#if( $ja4c ne '') {$ja4c_list{$ja4c} = 'x';}
			#if( $ja3c ne '') {$ja3c_list{$ja3c} = 'x';}
			#if( $tlsfp ne '') {$tlsfp_list{$tlsfp} = 'x';}
			#if( $tlsv ne '') {$tlsv_list{$tlsv} = 'x';}
			#if( $risk ne '') {$risk_list{$risk} = 'x';}

			if( ($in{l3proto} eq '' || $in{l3proto} eq '*' || $in{l3proto} eq $l3proto) &&
			    ($in{l4proto} eq '' || $in{l4proto} eq '*' || $in{l4proto} eq $l4proto) &&
			    ($in{src} eq '' || $in{src} eq '*' || $in{src} eq $src) &&
			    ($in{sport} eq '' || $in{sport} eq '*' || $in{sport} eq $sport) &&
			    ($in{dst} eq '' || $in{dst} eq '*' || $in{dst} eq $dst) &&
			    ($in{dport} eq '' || $in{dport} eq '*' || $in{dport} eq $dport) &&
			    ($in{ubytes} eq '' || $in{ubytes} eq '*' || $in{ubytes} eq $ubytes) &&
			    ($in{dbytes} eq '' || $in{dbytes} eq '*' || $in{dbytes} eq $dbytes) &&
			    ($in{upackets} eq '' || $in{upackets} eq '*' || $in{upackets} eq $upackets) &&
			    ($in{dpackets} eq '' || $in{dpackets} eq '*' || $in{dpackets} eq $dpackets) &&
			    ($in{ifindex} eq '' || $in{ifindex} eq '*' || $in{ifindex} eq $ifindex) &&
			    ($in{connmark} eq '' || $in{connmark} eq '*' || $in{connmark} eq $connmark) &&
			    ($in{srcnat} eq '' || $in{srcnat} eq '*' || $in{srcnat} eq $srcnat) &&
			    ($in{dstnat} eq '' || $in{dstnat} eq '*' || $in{dstnat} eq $dstnat) &&
			    ($in{proto} eq '' || $in{proto} eq '*' || $in{proto} eq $proto) &&
			    ($in{host} eq '' || $in{host} eq '*' || $in{host} eq $host) &&
			    ($in{ja4c} eq '' || $in{ja4c} eq '*' || $in{ja4c} eq $ja4c) &&
			    ($in{ja3c} eq '' || $in{ja3c} eq '*' || $in{ja3c} eq $ja3c) &&
			    ($in{tlsfp} eq '' || $in{tlsfp} eq '*' || $in{tlsfp} eq $tlsfp) &&
			    ($in{tlsv} eq '' || $in{tlsv} eq '*' || $in{tlsv} eq $tlsv) &&
			    ($in{risk} eq '' || $in{risk} eq '*' || $in{risk} eq $risk) ) {
				$count++;

				if( $count >= ($pag-1) * $pagelen && $count < $pag * $pagelen) {
					push @buffer, [$stime, $etime, $l3proto, $l4proto, $src, $sport, $dst, $dport,
					      		$ubytes, $dbytes, $upackets, $dpackets, $ifindex,
						       	$connmark, $srcnat, $dstnat, $proto, $host,
						       	$ja4c, $ja3c, $tlsfp, $tlsv, $risk];
				}
			}
	}
	close( LOG );

	# Pages index
	my $urlparam = 'stime='.$in{stime}.'&etime='.$in{etime}.'&l3proto='.$in{l3proto}.'&l4proto='.$in{l4proto}.
			'&src='.$in{src}.'&sport='.$in{sport}.'&dst='.$in{dst}.'&dport='.$in{dport}.'&ubytes='.$in{ubytes}.'&dbytes='.$in{dbytes}.
			'&upackets='.$in{upackets}.'&dpackets='.$in{dpackets}.'&ifindex='.$in{ifindex}.
			'&connmark='.$in{connmark}.'&srcnat='.$in{srcnat}.'&dstnat='.$in{dstnat}.
			'&proto='.$in{proto}.'&host='.$in{host}.'&ja4c='.$in{ja4c}.'&ja3c='.$in{ja3c}.
			'&tlsfp='.$in{tlsfp}.'&tlsv='.$in{tlsv}.'&risk='.$in{risk};
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
	print "<center>$pageindex</center>\n";

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

	local $hproto;
	$hproto .= "<b>ndpiPROTO<br></b>";
	push(@head, $hproto );

	local $hhost;
	$hhost .= "<b>HOSTNAME<br></b>";
	push(@head, $hhost );

	local $hsrc;
	$hsrc .= "<b>srcADDR<br><select name='src' size='1'>";
	foreach $opz (sort keys %src_list) {$hsrc .= "<option".($in{src} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hsrc .= "</select></b>";
	push(@head, $hsrc );

	local $hsport;
	$hsport .= "<b>srcPORT<br></b>";
	push(@head, $hsport );

	local $hdst;
	$hdst .= "<b>dstADDR<br></b>";
	push(@head, $hdst );

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

	local $hja3c;
	$hja3c .= "<b>ja3cFINGERPRINT<br></b>";
	push(@head, $hja3c );

	local $htlsfp;
	$htlsfp .= "<b>tlsFINGERPRINT<br></b>";
	push(@head, $htlsfp );

	local $htlsv;
	$htlsv .= "<b>tlsVERSION<br></b>";
	push(@head, $htlsv );

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
		 "style=white-space:nowrap",
		 "style=text-align:center",
		 "style=white-space:nowrap" );
	print &ui_columns_start(\@head, 100, 0, \@tds);

	foreach my $l (@buffer) {
		local @cols;
		my ($stime, $etime, $l3proto, $l4proto, $src, $sport, $dst, $dport, $ubytes, $dbytes, $upackets, $dpackets, $ifindex,
		    $connmark, $srcnat, $dstnat, $proto, $host, $ja4c, $ja3c, $tlsfp, $tlsv, $risk) = @$l;
	    	&showTD(localtime($stime)->strftime('%b %d %X'));
	    	&showTD(localtime($etime)->strftime('%b %d %X'));
		&showTD(&l3protoname($l3proto));
		&showTD(&l4protoname($l4proto));
		&showTD($proto);
		&showTD($host);
		&showTD($src);
		&showTD($sport);
		&showTD($dst);
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
		&showTD($ja3c);
		&showTD($tlsfp);
		&showTD($tlsv);
		&showTD(&getrisknames($risk));
	        print &ui_columns_row(\@cols, \@tds);
	}
	print &ui_columns_end();

	print "<table width=100%><tr>";
	print '<td style=text-align:right>'.&ui_submit( $text{'log_update'} ).'</td>';
	print "</tr></table>";

	print &ui_form_end();

	print "<center>$pageindex</center>\n";
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
