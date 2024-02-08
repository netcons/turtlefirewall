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

&ui_print_header( $text{'list_rules_title'}, $text{'title'}, "" );

showRule();

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showRule {
	print &ui_form_start("save_rule.cgi", "post");
	@links = ( &select_all_link("d"),
       		   &select_invert_link("d"),
		   "<a href=\"edit_rule.cgi?new=1\">$text{'list_rules_create_rule'}</a>" );
	@tds = ( 
		"width=1%",
		"width=1% align=center valign=center",
		"valign=top",
		"valign=top",
		"align=center valign=top style='white-space: normal;'",
		"align=center valign=top style='white-space: normal;'",
		"align=center valign=top style='white-space: normal;'",
		"align=center valign=top style='white-space: normal;'",
		"align=center valign=top style='white-space: normal;'",
		"valign=top",
		"valign=top",
		"valign=top",
		"width=1% valign=top" );
        print &ui_columns_start([
			'',
			"<b>#<b>",
                        "<b>$text{'rule_src'}</b>",
			"<b>$text{'rule_dst'}</b>",
			"<b>$text{'rule_service_head'}</b>",
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
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</strike></font>' : '';		# StrikeEnd
		my $aimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-yes.png hspace=4>' : '<img src=images/yes.png hspace=4>';
		my $dimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-no.png hspace=4>' : '<img src=images/no.png hspace=4>';
		my $rimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-exclamation.png hspace=4>' : '<img src=images/exclamation.png hspace=4>';
		my $rlimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-arrow.png hspace=4>' : '<img src=images/arrow.png hspace=4>';
		my $cimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-clock.png hspace=4>' : '<img src=images/clock.png hspace=4>';
		my $limage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-eye.png hspace=4>' : '<img src=images/eye.png hspace=4>';
		my $href = &ui_link("edit_rule.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
		push(@cols, $href );
		$attr{'SRC'} =~ s/,/, /g;
		push(@cols, "${sb}${bb}".$attr{'SRC'}."${be}${se}" );
		$attr{'DST'} =~ s/,/, /g;
		push(@cols, "${sb}${bb}".$attr{'DST'}."${be}${se}" );
		$attr{'SERVICE'} =~ s/,/, /g;
		local $serviceline;
		$serviceline .= "port (".$attr{'SERVICE'}."";
		if( $attr{'SERVICE'} eq 'tcp' || $attr{'SERVICE'} eq 'udp' ) {
			if( $attr{'PORT'} ne '' ) {
				$serviceline .= "/".$attr{'PORT'}."";
			} else {
				$serviceline .= "/all";
			}
		}
		$serviceline .= ")";
		my $cb = $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</font>' : '';			# ColourEnd
		if( $attr{'CATEGORY'} ne '' ) { 
			$serviceline .= " ndpi category (${cb}".$attr{'CATEGORY'}."${ce})"; 
		} elsif( $attr{'NDPI'} ne  '' ) {
			$attr{'NDPI'} =~ s/,/, /g;
			$serviceline .= " ndpi (${cb}".$attr{'NDPI'}."${ce})"; 
		}
		push(@cols, "${sb}${bb}".$serviceline."${be}${se}");
		if( $attr{'HOSTNAMESET'} eq '' ) { $attr{'HOSTNAMESET'} = 'any'; }
		my $cb = $attr{'HOSTNAMESET'} ne 'any' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'HOSTNAMESET'} ne 'any' && $se eq '' ? '</font>' : '';			# ColourEnd
		push(@cols, "${sb}${bb}${cb}".$attr{'HOSTNAMESET'}."${ce}${be}${se}" );
		if( $attr{'RISKSET'} eq '' ) { $attr{'RISKSET'} = 'none'; $rimage = ''; }
		my $cb = $attr{'RISKSET'} ne 'none' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'RISKSET'} ne 'none' && $se eq '' ? '</font>' : '';		# ColourEnd
		push(@cols, "${rimage}${sb}${bb}${cb}".$attr{'RISKSET'}."${ce}${be}${se}" );
		if( $attr{'RATELIMIT'} eq '' ) { $attr{'RATELIMIT'} = 'none'; $rlimage = ''; }
		my $cb = $attr{'RATELIMIT'} ne 'none' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'RATELIMIT'} ne 'none' && $se eq '' ? '</font>' : '';			# ColourEnd
		push(@cols, "${rlimage}${sb}${bb}${cb}".$attr{'RATELIMIT'}."${ce}${be}${se}" );
		if( $attr{'TIME'} eq '' ) { $attr{'TIME'} = 'always'; $cimage = ''; }
		my $cb = $attr{'TIME'} ne 'always' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'TIME'} ne 'always' && $se eq '' ? '</font>' : '';		# ColourEnd
		push(@cols, "${cimage}${sb}${bb}${cb}".$attr{'TIME'}."${ce}${be}${se}" );
 		if( $attr{'TARGET'} eq 'ACCEPT' ) {
			my $cb = $sb eq '' ? '<font color=green>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';		# ColourEnd
			push(@cols, "${aimage}${sb}${bb}${cb}".$attr{'TARGET'}."${ce}${be}${se}" );
		} else {
			my $cb = $sb eq '' ? '<font color=red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';		# ColourEnd
			push(@cols, "${dimage}${sb}${bb}${cb}".$attr{'TARGET'}."${ce}${be}${se}" );
		}
                if( $attr{'LOG'} eq 'YES' ) {
			my $cb = $sb eq '' ? '<font color=steelblue>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';           		# ColourEnd
			push(@cols, "${limage}${sb}${bb}${cb}".($attr{'TARGET'} eq 'ACCEPT' ? 'FLO' : 'ACT')."${ce}${be}${se}" );
                } else {
			push(@cols, '&nbsp;' );
		}
		push(@cols, "${sb}${bb}".($attr{'DESCRIPTION'} ne '' ? $attr{'DESCRIPTION'} : '&nbsp;')."${be}${se}" );
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
	print &ui_columns_row([undef, undef, "*", "*", "port (all)", "any", "none", "none", "always", "<img src='images/no.png' hspace='4'><font color=red>DROP</font>", "<img src='images/eye.png' hspace='4'><font color=steelblue>ACT</font>", "Implicit Deny", undef], \@tds);
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
