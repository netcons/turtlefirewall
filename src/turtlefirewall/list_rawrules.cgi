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

&ui_print_header( "$icons{HELPER}{IMAGE}$text{'list_rawrules_title'}", $text{'title'}, "" );

$form = 0;
showConntrackPreroute();

$form++;
print "<br><br>";
showConntrack();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showConntrackPreroute {
	print &ui_subheading($icons{HELPER}{IMAGE},$text{'conntrack_preroute'});
	print &ui_form_start("save_conntrackpreroute.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_conntrackpreroute.cgi?new=1\">$text{'list_conntrackpreroutes_create_rule'}</a>" );
	@tds = ( 
		"width=1% style=vertical-align:top",
		"width=1% style=vertical-align:top",
		"width=25% style=vertical-align:top;white-space:normal",
		"width=25% style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"width=1% style=vertical-align:top;white-space:normal",
		"width=1% style=vertical-align:top" );
        print &ui_columns_start([
			'',
			"<b>ID<b>",
                        "<b>$text{'rule_src'}</b>",
			"<b>$text{'rule_dst'}</b>",
			"<b>$text{'rule_service'}</b>",
			"<b>$text{'rule_helper'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nConntrackPreroutes = $fw->GetConntrackPreroutesCount();

	my $idx = $in{idx};
	if( $in{table} eq 'conntrackpreroute' ) {
		if( $in{down} > 0 || $in{up} > 0 ) {
			my $newIdx = $idx;
			if( $in{down} > 0 && $idx > 0 && $idx < $nConntrackPreroutes ) {
				$newIdx = $idx + $in{down};
				if( $newIdx > $nConntrackPreroutes ) { $newIdx = $nConntrackPreroutes; }
			}
			if( $in{up} > 0 && $idx > 1 && $idx <= $nConntrackPreroutes ) {
				$newIdx = $idx - $in{up};
				if( $newIdx < 1 ) { $newIdx = 1; }
			}
			$fw->MoveConntrackPreroute( $idx, $newIdx );
			$fw->SaveFirewall();
			$idx=$newIdx;
		}
	}

	for( my $i=1; $i<=$nConntrackPreroutes; $i++ ) {
		my %attr = $fw->GetConntrackPreroute($i);
		local @cols;
		if( $attr{'TARGET'} eq '' ) { $attr{'TARGET'} = 'ACCEPT'; }
		my $bb = $idx == $i && $in{table} eq 'conntrackpreroute' ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i && $in{table} eq 'conntrackpreroute' ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_conntrackpreroute.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
		push(@cols, $href );
		my $type = '';
		$type = $fw->GetItemType($attr{'SRC'});
		push(@cols, "$icons{$type}{IMAGE}${sb}${bb}$attr{'SRC'}${be}${se}" );
		$type = $fw->GetItemType($attr{'DST'});
		push(@cols, "$icons{$type}{IMAGE}${sb}${bb}$attr{'DST'}${be}${se}" );
		if( $attr{'PORT'} ne '' ) {
			push(@cols, "$icons{SERVICE}{IMAGE}${sb}${bb}$attr{'SERVICE'}/$attr{'PORT'}${be}${se}");
		} else {
			push(@cols, "$icons{SERVICE}{IMAGE}${sb}${bb}$attr{'SERVICE'}/all${be}${se}");
		}
		my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</span>' : '';           		# ColourEnd
		my $himage = $attr{'ACTIVE'} eq 'NO' ? $icons{HELPER}{IMAGE} : $icons{HELPER_A}{IMAGE};
		push(@cols, "${himage}${sb}${bb}${cb}".($attr{'HELPER'} ne '' ? $attr{'HELPER'} : '&nbsp;')."${ce}${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		if( $i < $nConntrackPreroutes ) {
			$mover .= "<td width=50%><a href='list_rawrules.cgi?table=conntrackpreroute&idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='v'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_rawrules.cgi?table=conntrackpreroute&idx=$i&up=1'>
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

sub showConntrack {
	print &ui_subheading($icons{HELPER}{IMAGE},$text{'conntrack'});
	print &ui_form_start("save_conntrack.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_conntrack.cgi?new=1\">$text{'list_conntracks_create_rule'}</a>" );
	@tds = ( 
		"width=1% style=vertical-align:top",
		"width=1% style=vertical-align:top",
		"width=25% style=vertical-align:top;white-space:normal",
		"width=25% style=vertical-align:top;white-space:normal",
		"style=vertical-align:top;white-space:normal",
		"width=1% style=vertical-align:top;white-space:normal",
		"width=1% style=vertical-align:top" );
        print &ui_columns_start([
			'',
			"<b>ID<b>",
                        "<b>$text{'rule_src'}</b>",
			"<b>$text{'rule_dst'}</b>",
			"<b>$text{'rule_service'}</b>",
			"<b>$text{'rule_helper'}</b>",
			"<b>$text{'rule_move'}</b>" ], 100, 0, \@tds);

	my $nConntracks = $fw->GetConntracksCount();

	my $idx = $in{idx};
	if( $in{table} eq 'conntrack' ) {
		if( $in{down} > 0 || $in{up} > 0 ) {
			my $newIdx = $idx;
			if( $in{down} > 0 && $idx > 0 && $idx < $nConntracks ) {
				$newIdx = $idx + $in{down};
				if( $newIdx > $nConntracks ) { $newIdx = $nConntracks; }
			}
			if( $in{up} > 0 && $idx > 1 && $idx <= $nConntracks ) {
				$newIdx = $idx - $in{up};
				if( $newIdx < 1 ) { $newIdx = 1; }
			}
			$fw->MoveConntrack( $idx, $newIdx );
			$fw->SaveFirewall();
			$idx=$newIdx;
		}
	}

	for( my $i=1; $i<=$nConntracks; $i++ ) {
		my %attr = $fw->GetConntrack($i);
		local @cols;
		if( $attr{'TARGET'} eq '' ) { $attr{'TARGET'} = 'ACCEPT'; }
		my $bb = $idx == $i && $in{table} eq 'conntrack' ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i && $in{table} eq 'conntrack' ? '</b>' : '';	# BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_conntrack.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
		push(@cols, $href );
		my $type = '';
		$type = $fw->GetItemType($attr{'SRC'});
		push(@cols, "$icons{$type}{IMAGE}${sb}${bb}$attr{'SRC'}${be}${se}" );
		$type = $fw->GetItemType($attr{'DST'});
		push(@cols, "$icons{$type}{IMAGE}${sb}${bb}$attr{'DST'}${be}${se}" );
		if( $attr{'PORT'} ne '' ) {
			push(@cols, "$icons{SERVICE}{IMAGE}${sb}${bb}$attr{'SERVICE'}/$attr{'PORT'}${be}${se}");
		} else {
			push(@cols, "$icons{SERVICE}{IMAGE}${sb}${bb}$attr{'SERVICE'}/all${be}${se}");
		}
		my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</span>' : '';           		# ColourEnd
		my $himage = $attr{'ACTIVE'} eq 'NO' ? $icons{HELPER}{IMAGE} : $icons{HELPER_A}{IMAGE};
		push(@cols, "${himage}${sb}${bb}${cb}".($attr{'HELPER'} ne '' ? $attr{'HELPER'} : '&nbsp;')."${ce}${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		if( $i < $nConntracks ) {
			$mover .= "<td width=50%><a href='list_rawrules.cgi?table=conntrack&idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='v'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_rawrules.cgi?table=conntrack&idx=$i&up=1'>
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
