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

&ui_print_header( "<img src=images/filter.png hspace=4>$text{'list_rules_title'}", $text{'title'}, "" );

&showRule();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showRule {
	print &ui_form_start("save_rule.cgi", "post");
	@links = ( &select_all_link("d"),
       		   &select_invert_link("d"),
		   "<a href=\"edit_rule.cgi?new=1\">$text{'list_rules_create_rule'}</a>" );
	@tds = ( 
		"width=1% style=vertical-align:top",
		"width=1% style=text-align:center;vertical-align:top",
		"width=10% style=vertical-align:top;white-space:normal",
		"width=10% style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"width=5% style=vertical-align:top;white-space:normal",
		"width=5% style=vertical-align:top;white-space:normal",
		"width=5% style=vertical-align:top;white-space:normal",
		"width=5% style=vertical-align:top;white-space:normal",
		"style=vertical-align:top",
		"style=vertical-align:top",
		"style=vertical-align:top;white-space:normal",
		"width=1% style=vertical-align:top" );
        print &ui_columns_start([
			'',
			"<b>ID<b>",
                        "<b>$text{'rule_src'}</b>",
			"<b>$text{'rule_dst'}</b>",
			"<b>$text{'rule_service'}</b>",
			"<b>$text{'rule_ndpi'}</b>",
			"<b>$text{'rule_hostname_set'}</b>",
			"<b>$text{'rule_risk_set'}</b>",
			"<b>$text{'rule_rate_limit'}</b>",
			"<b>$text{'rule_time'}</b>",
			"<b>$text{'rule_target'}</b>",
			"<b>$text{'rule_log'}</b>",
                        "<b>$text{'description'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nRules = $fw->GetRulesCount();

	my $idx = $in{idx};
	if( $in{down} > 0 || $in{up} > 0 ) {
		my $newIdx = $idx;
		if( $in{down} > 0 && $idx > 0 && $idx < $nRules ) {
			$newIdx = $idx + $in{down};
			if( $newIdx > $nRules ) { $newIdx = $nRules; }

			#my %appo = $fw->GetRule($newIdx);
			#$fw->AddRuleAttr($newIdx, $fw->GetRule($idx));
			#$fw->AddRuleAttr($idx, %appo);
			#$idx=$newIdx;
			#$fw->SaveFirewall();
		}
		if( $in{up} > 0 && $idx > 1 && $idx <= $nRules ) {
			$newIdx = $idx - $in{up};
			if( $newIdx < 1 ) { $newIdx = 1; }
			#my %appo = $fw->GetRule($newIdx);
			#$fw->AddRuleAttr($newIdx, $fw->GetRule($idx));
			#$fw->AddRuleAttr($idx, %appo);
		}
		$fw->MoveRule( $idx, $newIdx );
		$fw->SaveFirewall();
		$idx=$newIdx;
	}

	for( my $i=1; $i<=$nRules; $i++ ) {
		my %attr = $fw->GetRule($i);
		local @cols;
		if( $attr{'TARGET'} eq '' ) { $attr{'TARGET'} = 'ACCEPT'; }
		my $bb = $idx == $i ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_rule.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
		push(@cols, $href );
		my $srclist = '';
		my @srcs = split(/,/, $attr{'SRC'});
		foreach my $s (@srcs) {
			my $zimage = '<img src=images/zone.png hspace=4>';
			if( $s eq 'FIREWALL' ) {
			       	$zimage = '<img src=images/firewall.png hspace=4>';
			} else {
				my $type = $fw->GetItemType($s);
				if( $type eq 'NET' ) { $zimage = '<img src=images/net.png hspace=4>'; }
				elsif( $type eq 'HOST' ) { $zimage = '<img src=images/host.png hspace=4>'; }
				elsif( $type eq 'GEOIP' ) { $zimage = '<img src=images/geoip.png hspace=4>'; }
				elsif( $type eq 'GROUP' ) { $zimage = '<img src=images/group.png hspace=4>'; }
				elsif( $type eq 'IPSET' ) { $zimage = '<img src=images/item.png hspace=4>'; }
			}
			$srclist .= "${zimage}${s}<br>";
		}
		push(@cols, "${sb}${bb}${srclist}${be}${se}" );
		my $dstlist = '';
		my @dsts = split(/,/, $attr{'DST'});
		foreach my $d (@dsts) {
			my $zimage = '<img src=images/zone.png hspace=4>';
			if( $d eq 'FIREWALL' ) {
			       	$zimage = '<img src=images/firewall.png hspace=4>';
			} else {
				my $type = $fw->GetItemType($d);
				if( $type eq 'NET' ) { $zimage = '<img src=images/net.png hspace=4>'; }
				elsif( $type eq 'HOST' ) { $zimage = '<img src=images/host.png hspace=4>'; }
				elsif( $type eq 'GEOIP' ) { $zimage = '<img src=images/geoip.png hspace=4>'; }
				elsif( $type eq 'GROUP' ) { $zimage = '<img src=images/group.png hspace=4>'; }
				elsif( $type eq 'IPSET' ) { $zimage = '<img src=images/item.png hspace=4>'; }
			}
			$dstlist .= "${zimage}${d}<br>";
		}
		push(@cols, "${sb}${bb}${dstlist}${be}${se}" );
		my $servicelist = '';
		my $simage = '<img src=images/service.png hspace=4>';
		if( $attr{'SERVICE'} eq 'tcp' || $attr{'SERVICE'} eq 'udp' ) {
			if( $attr{'PORT'} ne '' ) {
				$servicelist .= "${simage}$attr{'SERVICE'}/$attr{'PORT'}";
			} else {
				$servicelist .= "${simage}$attr{'SERVICE'}/all";
			}
		} else {
			my @services = split(/,/, $attr{'SERVICE'});
			foreach my $s (@services) {
				$servicelist .= "${simage}${s}<br>";
			}
		}
		push(@cols, "${sb}${bb}${servicelist}${be}${se}");
		my $ndpilist = '';
		my $cb = $sb eq '' ? '<span style=color:orange>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</span>' : '';			# ColourEnd
		my $nimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-ndpi.png hspace=4>' : '<img src=images/ndpi.png hspace=4>';
		if( $attr{'CATEGORY'} ne '' ) { 
			$ndpilist .= "${nimage}${cb}category: $attr{'CATEGORY'}${ce}"; 
		} elsif( $attr{'NDPI'} ne  '' ) {
			my @ndpis = split(/,/, $attr{'NDPI'});
			foreach my $n (@ndpis) {
				$ndpilist .= "${nimage}${cb}${n}${ce}<br>";
			}
		}
		push(@cols, "${sb}${bb}${ndpilist}${be}${se}");
		my $himage = $attr{'HOSTNAMESET'} eq '' ? '' : '<img src=images/hostnameset.png hspace=4>';
		push(@cols, "${himage}${sb}${bb}$attr{'HOSTNAMESET'}${be}${se}" );
		my $rimage = $attr{'RISKSET'} eq '' ? '' : '<img src=images/riskset.png hspace=4>';
		push(@cols, "${rimage}${sb}${bb}$attr{'RISKSET'}${be}${se}" );
		my $pimage = $attr{'RATELIMIT'} eq '' ? '' : '<img src=images/ratelimit.png hspace=4>';
		push(@cols, "${pimage}${sb}${bb}$attr{'RATELIMIT'}${be}${se}" );
		my $type = $fw->GetItemType($attr{'TIME'});
		my $cimage = $type eq 'TIMEGROUP' ? '<img src=images/timegroup.png hspace=4>' : '<img src=images/time.png hspace=4>';
		if( $attr{'TIME'} eq '' ) { $cimage = ''; }
		push(@cols, "${cimage}${sb}${bb}$attr{'TIME'}${be}${se}" );
 		if( $attr{'TARGET'} eq 'ACCEPT' ) {
			my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $aimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-yes.png hspace=4>' : '<img src=images/yes.png hspace=4>';
			push(@cols, "${aimage}${sb}${bb}${cb}$attr{'TARGET'}${ce}${be}${se}" );
		} elsif( $attr{'TARGET'} eq 'DROP' ) {
			my $cb = $sb eq '' ? '<span style=color:red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-no.png hspace=4>' : '<img src=images/no.png hspace=4>';
			push(@cols, "${dimage}${sb}${bb}${cb}$attr{'TARGET'}${ce}${be}${se}" );
		} elsif( $attr{'TARGET'} eq 'REJECT' ) {
			my $cb = $sb eq '' ? '<span style=color:red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-reject.png hspace=4>' : '<img src=images/reject.png hspace=4>';
			push(@cols, "${dimage}${sb}${bb}${cb}$attr{'TARGET'}${ce}${be}${se}" );
		}
                if( $attr{'LOG'} eq 'YES' ) {
			my $cb = $sb eq '' ? '<span style=color:steelblue>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';           		# ColourEnd
			my $limage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-eye.png hspace=4>' : '<img src=images/eye.png hspace=4>';
			push(@cols, "${limage}${sb}${bb}${cb}".($attr{'TARGET'} eq 'ACCEPT' ? 'FLO' : 'ACT')."${ce}${be}${se}" );
                } else {
			push(@cols, '&nbsp;' );
		}
		my $iimage = $attr{'DESCRIPTION'} eq '' ? '' : '<img src=images/info.png hspace=4>';
		push(@cols, "${iimage}${sb}${bb}".($attr{'DESCRIPTION'} ne '' ? $attr{'DESCRIPTION'} : '&nbsp;')."${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		#		if( $i < $nRules-1 ) {
		#			$mover .= "<td width=50%><a href='list_rules.cgi?idx=$i&down=5'><img src='images/down5.gif' border='0' hspace='1' vspace='0' alt='V'></a></td>";
		#		} else {
		#			$mover .= "<td width=50%><img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'></td>";
		#		}
		if( $i < $nRules ) {
			$mover .= "<td width=50%><a href='list_rules.cgi?idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='v'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_rules.cgi?idx=$i&up=1'>
				   <img src='images/up.gif' border='0' hspace='1' vspace='0' alt='^'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;'>
				   </td>";
		}
		#		if( $i > 2 ) {
		#		$mover .= "<td width=50%><a href='list_rules.cgi?idx=$i&up=5'><img src='images/up5.gif' border='0' hspace='1' vspace='0' alt='A'></a></td>";
		#	} else {
		#		$mover .= "<td width=50%><img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;'></td>";
		#	}
		$mover .= "</tr></table>";
		push(@cols, $mover);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $i);
	}
	print &ui_columns_row([undef, undef, "<img src=images/zone.png hspace=4>*", "<img src=images/zone.png hspace=4>*", "<img src=images/service.png hspace=4>all", "", "", "", "", "", "<img src='images/no.png' hspace='4'><span style=color:red>DROP</span>", "<img src='images/eye.png' hspace='4'><span style=color:steelblue>ACT</span>", "<img src=images/info.png hspace=4>Implicit Deny", undef], \@tds);
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
