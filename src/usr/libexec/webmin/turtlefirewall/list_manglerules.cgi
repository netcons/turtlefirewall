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

&ui_print_header( $text{'list_manglerules_title'}, $text{'title'}, "" );

$form = 0;
showConnmarkPreroute();

$form++;
print "<br><br>";
showConnmark();

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showConnmarkPreroute {
	print &ui_subheading($text{'connmark_preroute'});
	print &ui_form_start("save_connmarkpreroute.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_connmarkpreroute.cgi?new=1\">$text{'list_connmarkpreroutes_create_rule'}</a>" );
	@tds = ( 
		"width=1%",
		"width=1% align=center valign=center",
		"width=10% valign=top",
		"width=10% valign=top",
		"align=center valign=top",
		"width=1% align=center valign=center",
		"width=1% align=center valign=center",
		"width=1% align=center valign=center",
		"width=1% align=center valign=center",
		"width=1% valign=top" );
        print &ui_columns_start([
			'',
			"<b>#<b>",
                        "<b>$text{'rule_src'}</b>",
			"<b>$text{'rule_dst'}</b>",
			"<b>$text{'rule_service_head'}</b>",
			"<b>$text{'rule_hostname_set'}</b>",
			"<b>$text{'rule_risk_set'}</b>",
			"<b>$text{'rule_time'}</b>",
			"<b>$text{'rule_mark'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nConnmarkPreroutes = $fw->GetConnmarkPreroutesCount();

	if( $in{table} eq 'connmarkpreroute' ) {
		my $idx = $in{idx};
		if( $in{down} > 0 || $in{up} > 0 ) {
			my $newIdx = $idx;
			if( $in{down} > 0 && $idx > 0 && $idx < $nConnmarkPreroutes ) {
				$newIdx = $idx + $in{down};
				if( $newIdx > $nConnmarkPreroutes ) { $newIdx = $nConnmarkPreroutes; }
			}
			if( $in{up} > 0 && $idx > 1 && $idx <= $nConnmarkPreroutes ) {
				$newIdx = $idx - $in{up};
				if( $newIdx < 1 ) { $newIdx = 1; }
			}
			$fw->MoveConnmarkPreroute( $idx, $newIdx );
			$fw->SaveFirewall();
			$idx=$newIdx;
		}
	}

	for( my $i=1; $i<=$nConnmarkPreroutes; $i++ ) {
		my %attr = $fw->GetConnmarkPreroute($i);
		local @cols;
		if( $attr{'TARGET'} eq '' ) { $attr{'TARGET'} = 'ACCEPT'; }
		my $bb = $idx == $i ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</strike></font>' : '';		# StrikeEnd
		my $cimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-clock.png hspace=4>' : '<img src=images/clock.png hspace=4>';
		my $href = &ui_link("edit_connmarkpreroute.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
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
			$serviceline .= ", ndpi category (${cb}".$attr{'CATEGORY'}."${ce})"; 
		} elsif( $attr{'NDPI'} ne  '' ) {
			$attr{'NDPI'} =~ s/,/, /g;
			$serviceline .= ", ndpi (${cb}".$attr{'NDPI'}."${ce})"; 
		}
		push(@cols, "${sb}${bb}".$serviceline."${be}${se}");
		if( $attr{'HOSTNAMESET'} eq '' ) { $attr{'HOSTNAMESET'} = 'any'; }
		my $cb = $attr{'HOSTNAMESET'} ne 'any' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'HOSTNAMESET'} ne 'any' && $se eq '' ? '</font>' : '';			# ColourEnd
		push(@cols, "${sb}${bb}${cb}".$attr{'HOSTNAMESET'}."${ce}${be}${se}" );
		if( $attr{'RISKSET'} eq '' ) { $attr{'RISKSET'} = 'none'; }
		my $cb = $attr{'RISKSET'} ne 'none' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'RISKSET'} ne 'none' && $se eq '' ? '</font>' : '';		# ColourEnd
		push(@cols, "${sb}${bb}${cb}".$attr{'RISKSET'}."${ce}${be}${se}" );
		if( $attr{'TIME'} eq '' ) { $attr{'TIME'} = 'always'; $cimage = ''; }
		push(@cols, "${cimage}${sb}${bb}".$attr{'TIME'}."${be}${se}" );
		push(@cols, "${sb}${bb}".($attr{'MARK'} ne '' ? $attr{'MARK'} : '&nbsp;')."${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		#		if( $i < $nConnmarkPreroutes-1 ) {
		#			$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmarkpreroute&idx=$i&down=5'><img src='images/down5.gif' border='0' hspace='1' vspace='0' alt='V'></a></td>";
		#		} else {
		#			$mover .= "<td width=50%><img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'></td>";
		#		}
		if( $i < $nConnmarkPreroutes ) {
			$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmarkpreroute&idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='v'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmarkpreroute&idx=$i&up=1'>
				   <img src='images/up.gif' border='0' hspace='1' vspace='0' alt='^'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;'>
				   </td>";
		}
		#		if( $i > 2 ) {
		#		$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmarkpreroute&idx=$i&up=5'><img src='images/up5.gif' border='0' hspace='1' vspace='0' alt='A'></a></td>";
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

sub showConnmark {
	print &ui_subheading($text{'connmark'});
	print &ui_form_start("save_connmark.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_connmark.cgi?new=1\">$text{'list_connmarks_create_rule'}</a>" );
	@tds = ( 
		"width=1%",
		"width=1% align=center valign=center",
	 	"width=10% valign=top",
		"width=10% valign=top",
		"align=center valign=top",
		"width=1% align=center valign=center",
		"width=1% align=center valign=center",
		"width=1% align=center valign=center",
		"width=1% align=center valign=center",
		"width=1% valign=top" );
        print &ui_columns_start([
			'',
			"<b>#<b>",
                        "<b>$text{'rule_src'}</b>",
			"<b>$text{'rule_dst'}</b>",
			"<b>$text{'rule_service_head'}</b>",
			"<b>$text{'rule_hostname_set'}</b>",
			"<b>$text{'rule_risk_set'}</b>",
			"<b>$text{'rule_time'}</b>",
			"<b>$text{'rule_mark'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nConnmarks = $fw->GetConnmarksCount();

	if( $in{table} eq 'connmark' ) {
		my $idx = $in{idx};
		if( $in{down} > 0 || $in{up} > 0 ) {
			my $newIdx = $idx;
			if( $in{down} > 0 && $idx > 0 && $idx < $nConnmarks ) {
				$newIdx = $idx + $in{down};
				if( $newIdx > $nConnmarks ) { $newIdx = $nConnmarks; }
			}
			if( $in{up} > 0 && $idx > 1 && $idx <= $nConnmarks ) {
				$newIdx = $idx - $in{up};
				if( $newIdx < 1 ) { $newIdx = 1; }
			}
			$fw->MoveConnmark( $idx, $newIdx );
			$fw->SaveFirewall();
			$idx=$newIdx;
		}
	}

	for( my $i=1; $i<=$nConnmarks; $i++ ) {
		my %attr = $fw->GetConnmark($i);
		local @cols;
		if( $attr{'TARGET'} eq '' ) { $attr{'TARGET'} = 'ACCEPT'; }
		my $bb = $idx == $i ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</strike></font>' : '';		# StrikeEnd
		my $cimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-clock.png hspace=4>' : '<img src=images/clock.png hspace=4>';
		my $href = &ui_link("edit_connmark.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
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
			$serviceline .= ", ndpi category (${cb}".$attr{'CATEGORY'}."${ce})"; 
		} elsif( $attr{'NDPI'} ne  '' ) {
			$attr{'NDPI'} =~ s/,/, /g;
			$serviceline .= ", ndpi (${cb}".$attr{'NDPI'}."${ce})"; 
		}
		push(@cols, "${sb}${bb}".$serviceline."${be}${se}");
		if( $attr{'HOSTNAMESET'} eq '' ) { $attr{'HOSTNAMESET'} = 'any'; }
		my $cb = $attr{'HOSTNAMESET'} ne 'any' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'HOSTNAMESET'} ne 'any' && $se eq '' ? '</font>' : '';			# ColourEnd
		push(@cols, "${sb}${bb}${cb}".$attr{'HOSTNAMESET'}."${ce}${be}${se}" );
		if( $attr{'RISKSET'} eq '' ) { $attr{'RISKSET'} = 'none'; }
		my $cb = $attr{'RISKSET'} ne 'none' && $sb eq '' ? '<font color=orange>' : '';	# ColourBegin
		my $ce = $attr{'RISKSET'} ne 'none' && $se eq '' ? '</font>' : '';		# ColourEnd
		push(@cols, "${sb}${bb}${cb}".$attr{'RISKSET'}."${ce}${be}${se}" );
		if( $attr{'TIME'} eq '' ) { $attr{'TIME'} = 'always'; $cimage = ''; }
		push(@cols, "${cimage}${sb}${bb}".$attr{'TIME'}."${be}${se}" );
		push(@cols, "${sb}${bb}".($attr{'MARK'} ne '' ? $attr{'MARK'} : '&nbsp;')."${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		#		if( $i < $nConnmarks-1 ) {
		#			$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmark&idx=$i&down=5'><img src='images/down5.gif' border='0' hspace='1' vspace='0' alt='V'></a></td>";
		#		} else {
		#			$mover .= "<td width=50%><img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'></td>";
		#		}
		if( $i < $nConnmarks ) {
			$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmark&idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='v'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmark&idx=$i&up=1'>
				   <img src='images/up.gif' border='0' hspace='1' vspace='0' alt='^'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;'>
				   </td>";
		}
		#		if( $i > 2 ) {
		#		$mover .= "<td width=50%><a href='list_manglerules.cgi?table=connmark&idx=$i&up=5'><img src='images/up5.gif' border='0' hspace='1' vspace='0' alt='A'></a></td>";
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
