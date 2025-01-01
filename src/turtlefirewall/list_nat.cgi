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

&ui_print_header( "$icons{NAT}{IMAGE}$text{'list_nat_title'}", $text{'title'}, "" );

$form = 0;
&showNat();

$form++;
print "<br><br>";
&showMasquerade();

$form++;
print "<br><br>";
&showRedirect();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showNat {
	print &ui_subheading($icons{NAT}{IMAGE},$text{'nat'});
	print &ui_form_start("save_nat.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_nat.cgi?new=1\">$text{'list_nat_create_nat'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "width=1% style=text-align:center;vertical-align:top",
		 "width=25% style=vertical-align:top;white-space:normal",
		 "width=25% style=vertical-align:top;white-space:normal",
		 "style=vertical-align:top;white-space:normal",
		 "width=1% style=vertical-align:top;text-align:center",
		 "width=1% style=vertical-align:top;white-space:normal",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
                          "",
                          "<b>ID</b>",
                          "<b>$text{'virtual_host'}</b>",
                          "<b>$text{'real_host'}</b>",
                          "<b>$text{'nat_service'}</b>",
                          "<b>$text{'nat'}</b>",
                          "<b>$text{'nat_toport'}</b>",
		 	  "<b>$text{'nat_move'}</b>" ], 100, 0, \@tds);

	$nNat = $fw->GetNatsCount();

	my $idx = $in{idx};
	if( $in{table} eq 'nat' ) {
		if( $in{down} > 0 || $in{up} > 0 ) {
			my $newIdx = $idx;
			if( $in{down} > 0 && $idx > 0 && $idx < $nNat ) {
				$newIdx = $idx + $in{down};
				if( $newIdx > $nNat ) { $newIdx = $nNat; }
			}
			if( $in{up} > 0 && $idx > 1 && $idx <= $nNat ) {
				$newIdx = $idx - $in{up};
				if( $newIdx < 1 ) { $newIdx = 1; }
			}
			$fw->MoveNat( $idx, $newIdx );
			$fw->SaveFirewall();
			$idx=$newIdx;
		}
	}

	for( my $i=1; $i<=$nNat; $i++ ) {
		my %attr = $fw->GetNat( $i );
		local @cols;
		my $bb = $idx == $i && $in{table} eq 'nat' ? '<b>' : '';       # BoldBegin
		my $be = $idx == $i && $in{table} eq 'nat'? '</b>' : '';      # BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_nat.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
		push(@cols, $href );
		my %zone = $fw->GetZone($attr{'VIRTUAL'});
		if( $zone{IF} ne '' ) {
			push(@cols, "$icons{ZONE}{IMAGE}${sb}${bb}$attr{'VIRTUAL'} ($zone{'IF'})${be}${se}" );
		} else {
			push(@cols, "$icons{HOST}{IMAGE}${sb}${bb}$attr{'VIRTUAL'}${be}${se}" );
		}
		push(@cols, "$icons{HOST}{IMAGE}${sb}${bb}$attr{'REAL'}${be}${se}" );
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
		my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</span>' : '';           		# ColourEnd
		my $nimage = $attr{'ACTIVE'} eq 'NO' ? $icons{NAT}{IMAGE} : $icons{NAT_A}{IMAGE};
		push(@cols, "${nimage}${sb}${bb}${cb}$text{YES}${ce}${be}${se}" );
		my $timage = $attr{'TOPORT'} eq '' ? '' : $icons{TOPORT}{IMAGE};
		push(@cols, "${timage}${sb}${bb}$attr{'TOPORT'}${be}${se}" );
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";

		if( $i < $nNat ) {
			$mover .= "<td width=50%><a href='list_nat.cgi?table=nat&idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='down'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_nat.cgi?table=nat&idx=$i&up=1'>
				   <img src='images/up.gif' border='0' hspace='1' vspace='0' alt='up'></a>
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

sub showMasquerade {
	print &ui_subheading($icons{MASQUERADE}{IMAGE},$text{'masquerade'});
	print &ui_form_start("save_masquerade.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_masquerade.cgi?new=1\">$text{'list_nat_create_masq'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "width=1% style=text-align:center;vertical-align:top",
		 "width=25% style=vertical-align:top;white-space:normal",
		 "width=25% style=vertical-align:top;white-space:normal",
		 "style=vertical-align:top;white-space:normal",
		 "width=1% style=vertical-align:top;text-align:center",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
                          "",
                          "<b>ID</b>",
                          "<b>$text{'masq_src'}</b>",
                          "<b>$text{'masq_dst'}</b>",
                          "<b>$text{'masq_service'}</b>",
                          "<b>$text{'masq_masquerade'}</b>",
		 	  "<b>$text{'masq_move'}</b>" ], 100, 0, \@tds);

	my $nMasq = $fw->GetMasqueradesCount();
	
	my $idx = $in{idx};
	if( $in{table} eq 'masquerade' ) {
		if( $in{down} > 0 || $in{up} > 0 ) {
			my $newIdx = $idx;
			if( $in{down} > 0 && $idx > 0 && $idx < $nMasq ) {
				$newIdx = $idx + $in{down};
				if( $newIdx > $nMasq ) { $newIdx = $nMasq; }
			}
			if( $in{up} > 0 && $idx > 1 && $idx <= $nMasq ) {
				$newIdx = $idx - $in{up};
				if( $newIdx < 1 ) { $newIdx = 1; }
			}
			$fw->MoveMasquerade( $idx, $newIdx );
			$fw->SaveFirewall();
			$idx=$newIdx;
		}
	}

	for( my $i=1; $i<=$nMasq; $i++ ) {
		my %attr = $fw->GetMasquerade( $i );
		local @cols;
		my $bb = $idx == $i && $in{table} eq 'masquerade' ? '<b>' : '';       # BoldBegin
		my $be = $idx == $i && $in{table} eq 'masquerade' ? '</b>' : '';      # BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_masquerade.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
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
		if( $attr{'MASQUERADE'} eq 'NO' ) {
			my $cb = $sb eq '' ? '<span style=color:red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? $icons{MASQUERADE}{IMAGE} : $icons{MASQUERADE_NO}{IMAGE};
			push(@cols, "${dimage}${sb}${bb}${cb}$text{NO}${ce}${be}${se}" );
		} else {
			my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';			# ColourEnd
			my $aimage = $attr{'ACTIVE'} eq 'NO' ? $icons{MASQUERADE}{IMAGE} : $icons{MASQUERADE_A}{IMAGE};
			push(@cols, "${aimage}${sb}${bb}${cb}$text{YES}${ce}${be}${se}" );
		}
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		if( $i < $nMasq ) {
			$mover .= "<td width=50%><a href='list_nat.cgi?table=masquerade&idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='down'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_nat.cgi?table=masquerade&idx=$i&up=1'>
				   <img src='images/up.gif' border='0' hspace='1' vspace='0' alt='up'></a>
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

sub showRedirect {
	print &ui_subheading($icons{REDIRECT}{IMAGE},$text{'redirect_redirect'});
	print &ui_form_start("save_redirect.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_redirect.cgi?new=1\">$text{'list_nat_create_redirect'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "width=1% style=text-align:center;vertical-align:top",
		 "width=25% style=vertical-align:top;white-space:normal",
		 "width=25% style=vertical-align:top;white-space:normal",
		 "style=vertical-align:top;white-space:normal",
		 "width=1% style=vertical-align:top;text-align:center",
		 "width=1% style=vertical-align:top;white-space:normal",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
                          "",
                          "<b>ID</b>",
                          "<b>$text{'redirect_src'}</b>",
                          "<b>$text{'redirect_dst'}</b>",
                          "<b>$text{'redirect_service'}</b>",
                          "<b>$text{'redirect_redirect'}</b>",
                          "<b>$text{'redirect_toport'}</b>",
		 	  "<b>$text{'redirect_move'}</b>" ], 100, 0, \@tds);

	my $nRedirect = $fw->GetRedirectCount();

	my $idx = $in{idx};
	if( $in{table} eq 'redirect' ) {
		if( $in{down} > 0 || $in{up} > 0 ) {
			my $newIdx = $idx;
			if( $in{down} > 0 && $idx > 0 && $idx < $nRedirect ) {
				$newIdx = $idx + $in{down};
				if( $newIdx > $nRedirect ) { $newIdx = $nRedirect; }
			}
			if( $in{up} > 0 && $idx > 1 && $idx <= $nRedirect ) {
				$newIdx = $idx - $in{up};
				if( $newIdx < 1 ) { $newIdx = 1; }
			}
			$fw->MoveRedirect( $idx, $newIdx );
			$fw->SaveFirewall();
			$idx=$newIdx;
		}
	}

	for( my $i=1; $i<=$nRedirect; $i++ ) {
		my %attr = $fw->GetRedirect( $i );
		local @cols;
		my $bb = $idx == $i && $in{table} eq 'redirect' ? '<b>' : '';       # BoldBegin
		my $be = $idx == $i && $in{table} eq 'redirect' ? '</b>' : '';      # BoldEnd
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<s><span style=color:grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</s></span>' : '';		# StrikeEnd
		my $href = &ui_link("edit_redirect.cgi?idx=$i","${sb}${bb}${i}${be}${se}");
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
		if( $attr{'REDIRECT'} eq 'NO' ) {
			my $cb = $sb eq '' ? '<span style=color:red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? $icons{REDIRECT}{IMAGE} : $icons{REDIRECT_NO}{IMAGE};
			push(@cols, "${dimage}${sb}${bb}${cb}$text{NO}${ce}${be}${se}" );
			push(@cols, "" );
		} else {
			my $cb = $sb eq '' ? '<span style=color:green>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</span>' : '';			# ColourEnd
			my $aimage = $attr{'ACTIVE'} eq 'NO' ? $icons{REDIRECT}{IMAGE} : $icons{REDIRECT_A}{IMAGE};
			push(@cols, "${aimage}${sb}${bb}${cb}$text{YES}${ce}${be}${se}" );
			my $timage = $attr{'TOPORT'} eq '' ? '' : $icons{TOPORT}{IMAGE};
			push(@cols, "${timage}${sb}${bb}$attr{'TOPORT'}${be}${se}" );
		}
		local $mover;
		$mover .= "<table cellspacing=0 cellpadding=0><tr>";
		if( $i < $nRedirect ) {
			$mover .= "<td width=50%><a href='list_nat.cgi?table=redirect&idx=$i&down=1'>
				   <img src='images/down.gif' border='0' hspace='1' vspace='0' alt='down'></a>
				   </td>";
		} else {
			$mover .= "<td width=50%>
				   <img src='images/gap.gif' border='0' hspace='1' vspace='0' alt='&nbsp;&nbsp;&nbsp;&nbsp;'>
				   </td>";
		}
		if( $i > 1 ) {
			$mover .= "<td width=50%><a href='list_nat.cgi?table=redirect&idx=$i&up=1'>
				   <img src='images/up.gif' border='0' hspace='1' vspace='0' alt='up'></a>
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
