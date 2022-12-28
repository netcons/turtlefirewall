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

&ui_print_header( $text{'list_rawrules_title'}, $text{'title'}, "" );

showConntrackPreroute();

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showConntrackPreroute {
	print "<br><big><b>$text{conntrack_preroute}</b></big>";
	print &ui_form_start("save_conntrackpreroute.cgi", "post");
	@links = ( &select_all_link("d"),
       		   &select_invert_link("d"),
		   "<a href=\"edit_conntrackpreroute.cgi?new=1\">$text{'list_conntrackpreroutes_create_rule'}</a>" );
	@tds = ( 
		"width=1%",
		"width=1% align=center valign=center",
		"width=10% valign=top",
		"width=10% valign=top",
		"align=center valign=top",
		"width=1% align=center valign=center",
		"width=1% valign=top" );
        print &ui_columns_start([
			'',
			"<b>#<b>",
                        "<b>$text{'rule_src'}</b>",
			"<b>$text{'rule_dst'}</b>",
			"<b>$text{'rule_service_head'}</b>",
			"<b>$text{'rule_helper'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nConntrackPreroutes = $fw->GetConntrackPreroutesCount();

	my $idx = $in{idx};
	if( $in{down} > 0 || $in{up} > 0 ) {
		my $newIdx = $idx;
		if( $in{down} > 0 && $idx > 0 && $idx < $nConntrackPreroutes ) {
			$newIdx = $idx + $in{down};
			if( $newIdx > $nConntrackPreroutes ) { $newIdx = $nConntrackPreroutes; }

			#my %appo = $fw->GetRule($newIdx);
			#$fw->AddRuleAttr($newIdx, $fw->GetRule($idx));
			#$fw->AddRuleAttr($idx, %appo);
			#$idx=$newIdx;
			#$fw->SaveFirewall();
		}
		if( $in{up} > 0 && $idx > 1 && $idx <= $nConntrackPreroutes ) {
			$newIdx = $idx - $in{up};
			if( $newIdx < 1 ) { $newIdx = 1; }
			#my %appo = $fw->GetRule($newIdx);
			#$fw->AddRuleAttr($newIdx, $fw->GetRule($idx));
			#$fw->AddRuleAttr($idx, %appo);
		}
		$fw->MoveConntrackPreroute( $idx, $newIdx );
		$fw->SaveFirewall();
		$idx=$newIdx;
	}

	for( my $i=1; $i<=$nConntrackPreroutes; $i++ ) {
		my %attr = $fw->GetConntrackPreroute($i);
		local @cols;
		if( $attr{'TARGET'} eq '' ) { $attr{'TARGET'} = 'ACCEPT'; }
		my $bb = $idx == $i ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</strike></font>' : '';		# StrikeEnd
		my $cimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-clock.png hspace=4>' : '<img src=images/clock.png hspace=4>';
		my $href = &ui_link("edit_conntrackpreroute.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
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
		push(@cols, "${sb}${bb}".$serviceline."${be}${se}");
		push(@cols, "${sb}${bb}".($attr{'HELPER'} ne '' ? $attr{'HELPER'} : '&nbsp;')."${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		#		if( $i < $nConntrackPreroutes-1 ) {
		#			$mover .= "<td width=50%><a href='list_rawrules.cgi?idx=$i&down=5'><img src='images/down5.gif' border='0' hspace='1' vspace='0' alt='V'></a></td>";
		#		} else {
		#			$mover .= "<td width=50%><img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'></td>";
		#		}
		if( $i < $nConntrackPreroutes ) {
			$mover .= "<td width=50%><a href='list_rawrules.cgi?idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='v'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_rawrules.cgi?idx=$i&up=1'>
				   <img src='images/up.gif' border='0' hspace='1' vspace='0' alt='^'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;'>
				   </td>";
		}
		#		if( $i > 2 ) {
		#		$mover .= "<td width=50%><a href='list_rawrules.cgi?idx=$i&up=5'><img src='images/up5.gif' border='0' hspace='1' vspace='0' alt='A'></a></td>";
		#	} else {
		#		$mover .= "<td width=50%><img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;'></td>";
		#	}
		$mover .= "</tr></table>";
		push(@cols, $mover);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $i);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
