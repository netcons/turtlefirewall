#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

&header( $text{'title'}, '', undef, 1 );

print "<table border width=\"100%\">
	<tr $cb><td>";
showLog();
print "</td></tr></table>";

&footer('','turtle firewall index');

sub showLog {

	print "Using logfile $SysLogFile";

	my $pag = $in{pag};
	if( $pag == 0 ) { $pag = 1; }
	my $count = 0;
	my $pagelen = 40;
	my @buffer = ();

	my %chain_list = ('*'=>'x');
	my %in_list = ('*'=>'x');
	my %out_list = ('*'=>'x');
	my %mac_list = ('*'=>'x');
	my %src_list = ('*'=>'x');
	my %dst_list = ('*'=>'x');
	my %proto_list = ('*'=>'x');
	my %spt_list = ('*'=>'x');
	my %dpt_list = ('*'=>'x');

	open( LOG, "< ". $SysLogFile );
	while( <LOG> ) {
		if( $_ =~ /TFW / ) {
			my $l = $_;

			my $time = '';
			my $chain = '';
			my $in = '';
			my $out = '';
			my $mac = '';
			my $src = '';
			my $dst = '';
			my $proto = '';
			my $spt = '';
			my $dpt = '';

			# Gestisco sia i nuovi log "TFW" che i vecchi "TFW DROP".
			if( $l =~ /^(.*?\d\d\:\d\d\:\d\d) .*?TFW (.*?)\:/ ) {
				$time = $1;
				$chain = $2;
				$chain =~ s/^DROP //;
			}
			if( $l =~ /IN=(.*?) / ) { $in = $1; }
			if( $l =~ /OUT=(.*?) / ) { $out = $1; }
			if( $l =~ /MAC=(.*?) / ) { $mac = $1; }
			if( $l =~ /SRC=(.*?) / ) { $src = $1; }
			if( $l =~ /DST=(.*?) / ) { $dst = $1; }
			if( $l =~ /PROTO=(.*?) / ) { $proto = $1; }
			if( $l =~ /SPT=(.*?) / ) { $spt = $1; }
			if( $l =~ /DPT=(.*?) / ) { $dpt = $1; }

			if( $chain ne '' ) {$chain_list{$chain} = 'x';}
			if( $in ne '' ) {$in_list{$in} = 'x';}
			if( $out ne '' ) {$out_list{$out} = 'x';}
			if( $mac ne '' ) {$mac_list{$mac} = 'x';}
			if( $src ne '' ) {$src_list{$src} = 'x';}
			if( $dst ne '' ) {$dst_list{$dst} = 'x';}
			if( $proto ne '') {$proto_list{$proto} = 'x';}
			if( $spt ne '') {$spt_list{$spt} = 'x';}
			if( $dpt ne '') {$dpt_list{$dpt} = 'x';}

			if( ($in{chain} eq '' || $in{chain} eq '*' || $in{chain} eq $chain) &&
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
					push @buffer, [$time, $chain, $in, $out, $mac, $src, $dst, $proto, $spt, $dpt];
				}
			}
		}
	}
	close( LOG );

	# Pages index
	my $urlparam = 'chain='.$in{chain}.'&in='.$in{in}.'&out='.$in{out}.'&mac='.$in{mac}.
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

	print qq~<br><form name="formlog" action="log.cgi"><center>$pageindex<br><br></center>~;
	print qq~<table width="100%" border="1" cellspacing="1">\n~;

	my $opz;
	print qq~<tr $tb><th><small>DATE<br><input name="submit" type="submit" value="$text{log_refresh}"></small></th>~;
	print '<th><small>DROP<br><select name="chain" size="1">';
	foreach $opz (sort keys %chain_list) {print "<option".($in{chain} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>IN<br><select name="in" size="1">';
	foreach $opz (sort keys %in_list) {print "<option".($in{in} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>OUT<br><select name="out">';
	foreach $opz (sort keys %out_list) {print "<option".($in{out} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>MAC<br><select name="mac">';
	foreach $opz (sort keys %mac_list) {print "<option".($in{mac} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>SRC<br><select name="src">';
	foreach $opz (sort keys %src_list) {print "<option".($in{src} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>DST<br><select name="dst">';
	foreach $opz (sort keys %dst_list) {print "<option".($in{dst} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>PROTO<br><select name="proto">';
	foreach $opz (sort keys %proto_list) {print "<option".($in{proto} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>SPORT<br><select name="spt">';
	foreach $opz (sort keys %spt_list) {print "<option".($in{spt} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	print '<th><small>DPORT<br><select name="dpt">';
	foreach $opz (sort keys %dpt_list) {print "<option".($in{dpt} eq $opz ? ' SELECTED' : '').">$opz</option>";}
	print "</select></small></th>\n";

	foreach my $l (@buffer) {
		print "<tr $cb>";
		my ($time, $chain, $in, $out, $mac, $src, $dst, $proto, $spt, $dpt) = @$l;
		showTD( $time, 1 );
		showTD( $chain );
		showTD( $in, 1 );
		showTD( $out, 1 );
		showTD( $mac, 1 );
		showTD( $src );
		showTD( $dst );
		showTD( $proto, 1 );
		showTD( $spt );
		showTD( $dpt );
		print "</tr>\n";
	}
	print "</table>";

	print "</form>";

	print "<br><center>$pageindex</center><br>\n";

}

sub showTD {
	my $text = shift;
	my $center = shift;
	if( $text eq '' ) { $text = '&nbsp;'; }
	if( $center ) { print "<td align=\"center\">"; } else { print "<td>"; }
	print "<tt>$text</tt></td>";
}
