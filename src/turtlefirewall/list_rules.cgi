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

&ui_print_header( "$icons{SHIELD}{IMAGE}$text{'index_icon_rules'}", $text{'title'}, "" );

&showRule();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showRule {
	print &ui_subheading($icons{RULE}{IMAGE},$text{'rule'});
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
		}
		if( $in{up} > 0 && $idx > 1 && $idx <= $nRules ) {
			$newIdx = $idx - $in{up};
			if( $newIdx < 1 ) { $newIdx = 1; }
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
		my $type = '';
		my $srclist = '';
		my $dstlist = '';
		my @srcs = split(/,/, $attr{'SRC'});
		foreach my $s (@srcs) {
			$type = $fw->GetItemType($s);
			$srclist .= "$icons{$type}{IMAGE}$s<br>";
		}
		push(@cols, "${sb}${bb}${srclist}${be}${se}" );
		my @dsts = split(/,/, $attr{'DST'});
		foreach my $d (@dsts) {
			$type = $fw->GetItemType($d);
			$dstlist .= "$icons{$type}{IMAGE}$d<br>";
		}
		push(@cols, "${sb}${bb}${dstlist}${be}${se}" );
		my $servicelist = '';
		if( $attr{'SERVICE'} eq 'tcp' || $attr{'SERVICE'} eq 'udp' ) {
			if( $attr{'PORT'} ne '' ) {
				$servicelist .= "$icons{SERVICE}{IMAGE}$attr{'SERVICE'}/$attr{'PORT'}";
			} else {
				$servicelist .= "$icons{SERVICE}{IMAGE}$attr{'SERVICE'}/all";
			}
		} else {
			my @services = split(/,/, $attr{'SERVICE'});
			foreach my $s (@services) {
				$servicelist .= "$icons{SERVICE}{IMAGE}$s<br>";
			}
		}
		push(@cols, "${sb}${bb}${servicelist}${be}${se}");
		my $ndpilist = '';
		my $cb = $sb eq '' ? '<span style=color:orange>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</span>' : '';			# ColourEnd
		my $nimage = $attr{'ACTIVE'} eq 'NO' ? $icons{NDPISERVICE}{IMAGE} : $icons{NDPISERVICE_A}{IMAGE};
		if( $attr{'CATEGORY'} ne '' ) { 
			$ndpilist .= "${nimage}${cb}category: $attr{'CATEGORY'}${ce}"; 
		} elsif( $attr{'NDPI'} ne  '' ) {
			my @ndpis = split(/,/, $attr{'NDPI'});
			foreach my $n (@ndpis) {
				$ndpilist .= "${nimage}${cb}${n}${ce}<br>";
			}
		}
		push(@cols, "${sb}${bb}${ndpilist}${be}${se}");
		my $himage = $attr{'HOSTNAMESET'} eq '' ? '' : $icons{HOSTNAMESET}{IMAGE};
		push(@cols, "${himage}${sb}${bb}$attr{'HOSTNAMESET'}${be}${se}" );
		my $rimage = $attr{'RISKSET'} eq '' ? '' : $icons{RISKSET}{IMAGE};
		push(@cols, "${rimage}${sb}${bb}$attr{'RISKSET'}${be}${se}" );
		my $pimage = $attr{'RATELIMIT'} eq '' ? '' : $icons{RATELIMIT}{IMAGE};
		push(@cols, "${pimage}${sb}${bb}$attr{'RATELIMIT'}${be}${se}" );
		my $cimage = '';
		if( $attr{'TIME'} eq '' ) {
		       	$cimage = '';
	       	} else {
			$type = $fw->GetItemType($attr{'TIME'});
			$cimage = $icons{$type}{IMAGE};
		}
		push(@cols, "${cimage}${sb}${bb}$attr{'TIME'}${be}${se}" );
 		if( $attr{'TARGET'} eq 'ACCEPT' ) {
			my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $aimage = $attr{'ACTIVE'} eq 'NO' ? $icons{ACCEPT}{IMAGE} : $icons{ACCEPT_A}{IMAGE};
			push(@cols, "${aimage}${sb}${bb}${cb}$attr{'TARGET'}${ce}${be}${se}" );
		} elsif( $attr{'TARGET'} eq 'DROP' ) {
			my $cb = $sb eq '' ? '<span style=color:red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? $icons{DROP}{IMAGE} : $icons{DROP_A}{IMAGE};
			push(@cols, "${dimage}${sb}${bb}${cb}$attr{'TARGET'}${ce}${be}${se}" );
		} elsif( $attr{'TARGET'} eq 'REJECT' ) {
			my $cb = $sb eq '' ? '<span style=color:red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? $icons{REJECT}{IMAGE} : $icons{REJECT_A}{IMAGE};
			push(@cols, "${dimage}${sb}${bb}${cb}$attr{'TARGET'}${ce}${be}${se}" );
		}
                if( $attr{'LOG'} eq 'YES' ) {
			my $cb = $sb eq '' ? '<span style=color:steelblue>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';           		# ColourEnd
			my $limage = $attr{'ACTIVE'} eq 'NO' ? $icons{LOG}{IMAGE} : $icons{LOG_A}{IMAGE};
			push(@cols, "${limage}${sb}${bb}${cb}".($attr{'TARGET'} eq 'ACCEPT' ? 'FLO' : 'ACT')."${ce}${be}${se}" );
                } else {
			push(@cols, '&nbsp;' );
		}
		my $iimage = $attr{'DESCRIPTION'} eq '' ? '' : $icons{DESCRIPTION}{IMAGE};
		push(@cols, "${iimage}${sb}${bb}".($attr{'DESCRIPTION'} ne '' ? $attr{'DESCRIPTION'} : '&nbsp;')."${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
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
		$mover .= "</tr></table>";
		push(@cols, $mover);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $i);
	}
	print &ui_columns_row([undef, undef, "$icons{ZONE}{IMAGE}*", "$icons{ZONE}{IMAGE}*", "$icons{SERVICE}{IMAGE}all", "", "", "", "", "", "$icons{DROP_A}{IMAGE}<span style=color:red>DROP</span>", "$icons{LOG_A}{IMAGE}<span style=color:steelblue>ACT</span>", "$icons{DESCRIPTION}{IMAGE}Implicit Deny", undef], \@tds);
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
