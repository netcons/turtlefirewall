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

&ui_print_header( "<img src=images/grey-eye.png hspace=4>$text{'log_title'}", $text{'title'}, "" );

&showLog();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showLog {

	my $pag = $in{pag};
	if( $pag == 0 ) { $pag = 1; }
	my $count = 0;
	my $pagelen = 20;
	my @buffer = ();

	my %action_list = ('*' => undef);
	my %in_list = ('*' => undef);
	my %out_list = ('*' => undef);
	my %mac_list = ('*' => undef);
	my %src_list = ('*' => undef);
	my %dst_list = ('*' => undef);
	my %proto_list = ('*' => undef);
	my %spt_list = ('*' => undef);
	my %dpt_list = ('*' => undef);

	open( LOG, "<", $SysLogFile );
	while( <LOG> ) {
		if( $_ =~ /TFW=/ ) {
			my $l = $_;

			my $time = '';
			my $action = '';
			my $in = '';
			my $out = '';
			my $mac = '';
			my $src = '';
			my $dst = '';
			my $proto = '';
			my $spt = '';
			my $dpt = '';

			if( $l =~ /^(.*?\d\d\:\d\d\:\d\d) / ) {
				$time = $1;
			}
			if( $l =~ /TFW=(.*?) / ) { $action = $1; }
			if( $l =~ /IN=(.*?) / ) { $in = $1; }
			if( $l =~ /OUT=(.*?) / ) { $out = $1; }
			if( $l =~ /MAC=(.*?) / ) { $mac = $1; }
			if( $l =~ /SRC=(.*?) / ) { $src = $1; }
			if( $l =~ /DST=(.*?) / ) { $dst = $1; }
			if( $l =~ /PROTO=(.*?) / ) { $proto = $1; }
			if( $l =~ /SPT=(.*?) / ) { $spt = $1; }
			if( $l =~ /DPT=(.*?) / ) { $dpt = $1; }

			if( $action ne '' ) {$action_list{$action} = undef;}
			if( $in ne '' ) {$in_list{$in} = undef;}
			if( $out ne '' ) {$out_list{$out} = undef;}
			if( $mac ne '' ) {$mac_list{$mac} = undef;}
			if( $src ne '' ) {$src_list{$src} = undef;}
			if( $dst ne '' ) {$dst_list{$dst} = undef;}
			if( $proto ne '') {$proto_list{$proto} = undef;}
			if( $spt ne '') {$spt_list{$spt} = undef;}
			if( $dpt ne '') {$dpt_list{$dpt} = undef;}

			if( ($in{action} eq '' || $in{action} eq '*' || $in{action} eq $action) &&
			    ($in{in} eq '' || $in{in} eq '*' || $in{in} eq $in) &&
			    ($in{out} eq '' || $in{out} eq '*' || $in{out} eq $out) &&
			    ($in{mac} eq '' || $in{mac} eq '*' || $in{mac} eq $mac) &&
			    ($in{src} eq '' || $in{src} eq '*' || $in{src} eq $src) &&
			    ($in{dst} eq '' || $in{dst} eq '*' || $in{dst} eq $dst) &&
			    ($in{proto} eq '' || $in{proto} eq '*' || $in{proto} eq $proto) &&
			    ($in{spt} eq '' || $in{spt} eq '*' || $in{spt} eq $spt) &&
			    ($in{dpt} eq '' || $in{dpt} eq '*' || $in{dpt} eq $dpt) ) {
				$count++;

				if( $count >= ($pag-1) * $pagelen && $count < $pag * $pagelen) {
					push @buffer, [$time, $action, $in, $out, $mac, $src, $dst, $proto, $spt, $dpt];
				}
			}
		}
	}
	close( LOG );

	# Pages index
	my $urlparam = 'action='.$in{action}.'&in='.$in{in}.'&out='.$in{out}.'&mac='.$in{mac}.
			'&src='.$in{src}.'&dst='.$in{dst}.'&proto='.$in{proto}.
			'&spt='.$in{spt}.'&dpt='.$in{dpt};
	my $pageindex = '';
	if( $pag > 1 ) {
		$pageindex .= "&nbsp;<a href=\"log.cgi?pag=1&$urlparam\">&lt;&lt;</a>&nbsp;";
		$pageindex .= "&nbsp;<a href=\"log.cgi?pag=".($pag-1)."&$urlparam\">&lt;</a>&nbsp;";
	}
	$pageindex .= "&nbsp;(<b>$pag</b>)&nbsp;";
	$lastpag = int(($count-1) / $pagelen) + 1;
	if( $pag < $lastpag ) {
		$pageindex .= "&nbsp;<a href=\"log.cgi?pag=".($pag+1)."&$urlparam\">&gt;</a>&nbsp;";
		$pageindex .= qq~&nbsp;<a href="log.cgi?pag=$lastpag&$urlparam">&gt;&gt;</a>&nbsp;~;
	}

	print &ui_form_start("log.cgi", "post");
	print "<center>$pageindex</center>\n";

	my $opz;

	local @head;

        local $hdate;
        $hdate .= "<b>DATE<br></b>";
        push(@head, $hdate );

	local $haction;
	$haction .= "<b>ACTION<br><select name='action' size='1'>";
        foreach $opz (sort keys %action_list) {$haction .= "<option".($in{action} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$haction .= "</select></b>";
	push(@head, $haction );

	local $hin;
	$hin .= "<b>IN<br><select name='in' size='1'>";
        foreach $opz (sort keys %in_list) {$hin .= "<option".($in{in} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hin .= "</select></b>";
	push(@head, $hin );

	local $hout;
	$hout .= "<b>OUT<br><select name='out' size='1'>";
        foreach $opz (sort keys %out_list) {$hout .= "<option".($in{out} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hout .= "</select></b>";
	push(@head, $hout );

	local $hsrc;
	$hsrc .= "<b>SRC<br><select name='src' size='1'>";
        foreach $opz (sort keys %src_list) {$hsrc .= "<option".($in{src} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hsrc .= "</select></b>";
	push(@head, $hsrc );

	local $hdst;
	$hdst .= "<b>DST<br><select name='dst' size='1'>";
        foreach $opz (sort keys %dst_list) {$hdst .= "<option".($in{dst} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hdst .= "</select></b>";
	push(@head, $hdst );

	local $hproto;
	$hproto .= "<b>PROTO<br><select name='proto' size='1'>";
        foreach $opz (sort keys %proto_list) {$hproto .= "<option".($in{proto} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hproto .= "</select></b>";
	push(@head, $hproto );

	local $hspt;
	$hspt .= "<b>SPORT<br><select name='spt' size='1'>";
        foreach $opz (sort keys %spt_list) {$hspt .= "<option".($in{spt} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hspt .= "</select></b>";
	push(@head, $hspt );

	local $hdpt;
	$hdpt .= "<b>DPORT<br><select name='dpt' size='1'>";
        foreach $opz (sort keys %dpt_list) {$hdpt .= "<option".($in{dpt} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hdpt .= "</select></b>";
	push(@head, $hdpt );

	local $hmac;
	$hmac .= "<b>MAC<br><select name='mac' size='1'>";
        foreach $opz (sort keys %mac_list) {$hmac .= "<option".($in{mac} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	$hmac .= "</select></b>";
	push(@head, $hmac );

	@tds = ( "style=white-space:nowrap", "style=text-align:center", "style=text-align:center", "", "", "", "style=text-align:center", "", "", "" );
	print &ui_columns_start(\@head, 100, 0, \@tds);

	foreach my $l (@buffer) {
		local @cols;
		my ($time, $action, $in, $out, $mac, $src, $dst, $proto, $spt, $dpt) = @$l;
		&showTD($time);
		&showTD($action);
		&showTD($in);
		&showTD($out);
		&showTD($src);
		&showTD($dst);
		&showTD($proto);
		&showTD($spt);
		&showTD($dpt);
		&showTD($mac);
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
	push(@cols, "<i>$text</i>");
}
