#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';
&ReadParse();

&ui_print_header( "$icons{MARK}{IMAGE}$text{'list_manglerules_title'}", $text{'title'}, "" );

$form = 0;
&showConnmarkPreroute();

$form++;
print "<br><br>";
&showConnmark();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showConnmarkPreroute {
	print &ui_subheading($icons{MARK}{IMAGE},$text{'connmark_preroute'});
	print &ui_form_start("save_connmarkpreroute.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_connmarkpreroute.cgi?new=1\">$text{'list_connmarkpreroutes_create_rule'}</a>" );
	@tds = ( 
		"width=1% style=vertical-align:top",
		"width=1% style=vertical-align:top",
		"width=10% style=vertical-align:top;white-space:normal",
		"width=10% style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"width=5% style=vertical-align:top;white-space:normal",
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
			"<b>$text{'rule_time'}</b>",
			"<b>$text{'rule_mark'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nConnmarkPreroutes = $fw->GetConnmarkPreroutesCount();

	my $idx = $in{idx};
	if( $in{table} eq 'connmarkpreroute' ) {
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
		my $bb = $idx == $i && $in{table} eq 'connmarkpreroute' ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i && $in{table} eq 'connmarkpreroute' ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_connmarkpreroute.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
		push(@cols, $href );
		my $type = '';
		$type = $fw->GetItemType($attr{'SRC'});
		push(@cols, "$icons{$type}{IMAGE}${sb}${bb}$attr{'SRC'}${be}${se}" );
		$type = $fw->GetItemType($attr{'DST'});
		push(@cols, "$icons{$type}{IMAGE}${sb}${bb}$attr{'DST'}${be}${se}" );
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
		my $cimage = '';
		if( $attr{'TIME'} eq '' ) {
		       	$cimage = '';
	       	} else {
			$type = $fw->GetItemType($attr{'TIME'});
			$cimage = $icons{$type}{IMAGE};
		}
		push(@cols, "${cimage}${sb}${bb}$attr{'TIME'}${be}${se}" );
		my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</span>' : '';           		# ColourEnd
		my $mimage = $attr{'ACTIVE'} eq 'NO' ? $icons{MARK}{IMAGE} : $icons{MARK_A}{IMAGE};
		push(@cols, "${mimage}${sb}${bb}${cb}".($attr{'MARK'} ne '' ? $attr{'MARK'} : '&nbsp;')."${ce}${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
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
		$mover .= "</tr></table>";
		push(@cols, $mover);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $i);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}

sub showConnmark {
	print &ui_subheading($icons{MARK}{IMAGE},$text{'connmark'});
	print &ui_form_start("save_connmark.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_connmark.cgi?new=1\">$text{'list_connmarks_create_rule'}</a>" );
	@tds = ( 
		"width=1% style=vertical-align:top",
		"width=1% style=vertical-align:top",
	 	"width=10% style=vertical-align:top;white-space:normal",
		"width=10% style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"width=5% style=vertical-align:top;white-space:normal",
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
			"<b>$text{'rule_time'}</b>",
			"<b>$text{'rule_mark'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nConnmarks = $fw->GetConnmarksCount();

	my $idx = $in{idx};
	if( $in{table} eq 'connmark' ) {
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
		my $bb = $idx == $i && $in{table} eq 'connmark' ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i && $in{table} eq 'connmark' ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_connmark.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
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
		my $nimage = $attr{'ACTIVE'} eq 'NO' ? $icons{NDPISERVICE}{IMAGE}: $icons{NDPISERVICE_A}{IMAGE};
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
		my $cimage = '';
		if( $attr{'TIME'} eq '' ) {
		       	$cimage = '';
	       	} else {
			$type = $fw->GetItemType($attr{'TIME'});
			$cimage = $icons{$type}{IMAGE};
		}
		push(@cols, "${cimage}${sb}${bb}$attr{'TIME'}${be}${se}" );
		my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</span>' : '';           		# ColourEnd
		my $mimage = $attr{'ACTIVE'} eq 'NO' ? $icons{MARK}{IMAGE} : $icons{MARK_A}{IMAGE};
		push(@cols, "${mimage}${sb}${bb}${cb}".($attr{'MARK'} ne '' ? $attr{'MARK'} : '&nbsp;')."${ce}${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
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
		$mover .= "</tr></table>";
		push(@cols, $mover);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $i);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
