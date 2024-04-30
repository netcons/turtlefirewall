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

&ui_print_header( "<img src=images/grey-nat.png hspace=4>$text{'list_nat_title'}", $text{'title'}, "" );

$form = 0;
showNat();

$form++;
print "<br><br>";
showMasquerade();

$form++;
print "<br><br>";
showRedirect();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showNat {
	print &ui_subheading("<img src=images/grey-nat.png hspace=4>",$text{'nat'});
	print &ui_form_start("save_nat.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_nat.cgi?new=1\">$text{'list_nat_create_nat'}</a>" );
        @tds = ( "width=1% valign=top",
		 "width=1% align=center valign=center",
		 "width=10% valign=top style='white-space: normal;'",
		 "width=10% valign=top style='white-space: normal;'",
		 "valign=top style='white-space: normal;'",
		 "width=1% align=center valign=center",
		 "width=1% valign=top style='white-space: normal;'",
		 "width=1% valign=top" );
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

	if( $in{table} eq 'nat' ) {
		my $idx = $in{idx};
		if( $in{down} ne '' && $idx > 0 && $idx < $nNat ) {
			my %appo = $fw->GetNat($idx+1);
			$fw->AddNatAttr($idx+1, $fw->GetNat($idx));
			$fw->AddNatAttr($idx, %appo);
		}
		if( $in{up} ne '' && $idx > 1 && $idx <= $nNat ) {
			my %appo = $fw->GetNat($idx-1);
			$fw->AddNatAttr($idx-1, $fw->GetNat($idx));
			$fw->AddNatAttr($idx, %appo);
		}
		$fw->SaveFirewall();
	}

	for( my $i=1; $i<=$nNat; $i++ ) {
		my %attr = $fw->GetNat( $i );
		local @cols;
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</strike></font>' : '';		# StrikeEnd
		my $href = &ui_link("edit_nat.cgi?idx=$i","${sb}${i}${se}");
		push(@cols, $href );
		my %zone = $fw->GetZone($attr{'VIRTUAL'});
		if( $zone{IF} ne '' ) {
			my $zimage = '<img src=images/zone.png hspace=4>';
			push(@cols, "${zimage}${sb}".$attr{'VIRTUAL'}." (".$zone{'IF'}.")${se}" );
		} else {
			my $himage = '<img src=images/host.png hspace=4>';
			push(@cols, "${himage}${sb}".$attr{'VIRTUAL'}."${se}" );
		}
		my $himage = '<img src=images/host.png hspace=4>';
		push(@cols, "${himage}${sb}".$attr{'REAL'}."${se}" );
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
		my $simage = '<img src=images/service.png hspace=4>';
		push(@cols, "${simage}${sb}".$serviceline."${se}");
		my $cb = $sb eq '' ? '<font color=steelblue>' : '';	# ColourBegin
		my $ce = $se eq '' ? '</font>' : '';           		# ColourEnd
		my $nimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-nat.png hspace=4>' : '<img src=images/nat.png hspace=4>';
		push(@cols, "${nimage}${sb}${cb}".$text{YES}."${ce}${se}" );
		my $timage = $attr{'TOPORT'} eq '' ? '' : '<img src=images/toport.png hspace=4>';
		push(@cols, "${timage}${sb}".$attr{'TOPORT'}."${se}" );
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
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}

sub showMasquerade {
	print &ui_subheading("<img src=images/grey-nat.png hspace=4>",$text{'masquerade'});
	print &ui_form_start("save_masq.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_masq.cgi?new=1\">$text{'list_nat_create_masq'}</a>" );
        @tds = ( "width=1% valign=top",
		 "width=1% align=center valign=center",
		 "width=10% valign=top style='white-space: normal;'",
		 "width=10% valign=top style='white-space: normal;'",
		 "valign=top style='white-space: normal;'",
		 "width=1% align=center valign=center",
		 "width=1% valign=top" );
        print &ui_columns_start([
                          "",
                          "<b>ID</b>",
                          "<b>$text{'masq_src'}</b>",
                          "<b>$text{'masq_dst'}</b>",
                          "<b>$text{'masq_service'}</b>",
                          "<b>$text{'masq_masquerade'}</b>",
		 	  "<b>$text{'masq_move'}</b>" ], 100, 0, \@tds);

	my $nMasq = $fw->GetMasqueradesCount();
	
	if( $in{table} eq 'masquerade' ) {
		my $idx = $in{idx};
		if( $in{down} ne '' && $idx > 0 && $idx < $nMasq ) {
			my %appo = $fw->GetMasquerade($idx+1);
			$fw->AddMasqueradeAttr($idx+1, $fw->GetMasquerade($idx));
			$fw->AddMasqueradeAttr($idx, %appo);
		}
		if( $in{up} ne '' && $idx > 1 && $idx <= $nMasq ) {
			my %appo = $fw->GetMasquerade($idx-1);
			$fw->AddMasqueradeAttr($idx-1, $fw->GetMasquerade($idx));
			$fw->AddMasqueradeAttr($idx, %appo);
		}
		$fw->SaveFirewall();
	}	
	
	for( my $i=1; $i<=$nMasq; $i++ ) {
		my %attr = $fw->GetMasquerade( $i );
		local @cols;
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</strike></font>' : '';		# StrikeEnd
		my $href = &ui_link("edit_masq.cgi?idx=$i","${sb}${i}${se}");
		push(@cols, $href );
		my $zimage = '<img src=images/zone.png hspace=4>';
		my $type = $fw->GetItemType($attr{'SRC'});
		if( $type eq 'NET' ) { $zimage = '<img src=images/net.png hspace=4>'; }
		elsif( $type eq 'HOST' ) { $zimage = '<img src=images/host.png hspace=4>'; }
		elsif( $type eq 'GROUP' ) { $zimage = '<img src=images/group.png hspace=4>'; }
		push(@cols, "${zimage}${sb}".($attr{'SRC'} ne '' ? $attr{'SRC'} : '*')."${se}" );
		my $zimage = '<img src=images/zone.png hspace=4>';
		my $type = $fw->GetItemType($attr{'DST'});
                if( $type eq 'NET' ) { $zimage = '<img src=images/net.png hspace=4>'; }
		elsif( $type eq 'HOST' ) { $zimage = '<img src=images/host.png hspace=4>'; }
		elsif( $type eq 'GROUP' ) { $zimage = '<img src=images/group.png hspace=4>'; }
		push(@cols, "${zimage}${sb}".($attr{'DST'} ne '' ? $attr{'DST'} : '&nbsp;')."${se}" );
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
		my $simage = '<img src=images/service.png hspace=4>';
		push(@cols, "${simage}${sb}".$serviceline."${se}");
		if( $attr{'MASQUERADE'} eq 'NO' ) {
			my $cb = $sb eq '' ? '<font color=red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-nat.png hspace=4>' : '<img src=images/red-nat.png hspace=4>';
			push(@cols, "${dimage}${sb}${cb}".$text{NO}."${ce}${se}" );
		} else {
			my $cb = $sb eq '' ? '<font color=steelblue>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';			# ColourEnd
			my $aimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-nat.png hspace=4>' : '<img src=images/nat.png hspace=4>';
			push(@cols, "${aimage}${sb}${cb}".$text{YES}."${ce}${se}" );
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
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}

sub showRedirect {
	print &ui_subheading("<img src=images/grey-nat.png hspace=4>",$text{'redirect_redirect'});
	print &ui_form_start("save_redirect.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_redirect.cgi?new=1\">$text{'list_nat_create_redirect'}</a>" );
        @tds = ( "width=1% valign=top",
		 "width=1% align=center valign=center",
		 "width=10% valign=top style='white-space: normal;'",
		 "width=10% valign=top style='white-space: normal;'",
		 "valign=top style='white-space: normal;'",
		 "width=1% align=center valign=center",
		 "width=1% valign=top style='white-space: normal;'",
		 "width=1% valign=top" );
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
	if( $in{table} eq 'redirect' ) {
		my $idx = $in{idx};
		if( $in{down} ne '' && $idx > 0 && $idx < $nRedirect ) {
			my %appo = $fw->GetRedirect($idx+1);
			$fw->AddRedirectAttr($idx+1, $fw->GetRedirect($idx));
			$fw->AddRedirectAttr($idx, %appo);
		}
		if( $in{up} ne '' && $idx > 1 && $idx <= $nRedirect ) {
			my %appo = $fw->GetRedirect($idx-1);
			$fw->AddRedirectAttr($idx-1, $fw->GetRedirect($idx));
			$fw->AddRedirectAttr($idx, %appo);
		}
		$fw->SaveFirewall();
		#redirect( 'list_nat.cgi' );
	}

	for( my $i=1; $i<=$nRedirect; $i++ ) {
		my %attr = $fw->GetRedirect( $i );
		local @cols;
		my $sb = $attr{'ACTIVE'} eq 'NO' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $attr{'ACTIVE'} eq 'NO' ? '</strike></font>' : '';		# StrikeEnd
		my $href = &ui_link("edit_redirect.cgi?idx=$i","${sb}${i}${se}");
		push(@cols, $href );
		my $zimage = '<img src=images/zone.png hspace=4>';
		my $type = $fw->GetItemType($attr{'SRC'});
                if( $type eq 'NET' ) { $zimage = '<img src=images/net.png hspace=4>'; }
		elsif( $type eq 'HOST' ) { $zimage = '<img src=images/host.png hspace=4>'; }
		elsif( $type eq 'GROUP' ) { $zimage = '<img src=images/group.png hspace=4>'; }
		push(@cols, "${zimage}${sb}".$attr{'SRC'}."${se}" );
		my $zimage = '<img src=images/zone.png hspace=4>';
		my $type = $fw->GetItemType($attr{'DST'});
                if( $type eq 'NET' ) { $zimage = '<img src=images/net.png hspace=4>'; }
		elsif( $type eq 'HOST' ) { $zimage = '<img src=images/host.png hspace=4>'; }
		elsif( $type eq 'GROUP' ) { $zimage = '<img src=images/group.png hspace=4>'; }
		push(@cols, "${zimage}${sb}".$attr{'DST'}."${se}" );
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
		my $simage = '<img src=images/service.png hspace=4>';
		push(@cols, "${simage}${sb}".$serviceline."${se}");
		if( $attr{'REDIRECT'} eq 'NO' ) {
			my $cb = $sb eq '' ? '<font color=red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';		# ColourEnd
			my $dimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-nat.png hspace=4>' : '<img src=images/red-nat.png hspace=4>';
			push(@cols, "${dimage}${sb}${cb}".$text{NO}."${ce}${se}" );
		} else {
			my $cb = $sb eq '' ? '<font color=steelblue>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';			# ColourEnd
			my $aimage = $attr{'ACTIVE'} eq 'NO' ? '<img src=images/grey-nat.png hspace=4>' : '<img src=images/nat.png hspace=4>';
			push(@cols, "${aimage}${sb}${cb}".$text{YES}."${ce}${se}" );
		}
		my $timage = $attr{'TOPORT'} eq '' ? '' : '<img src=images/toport.png hspace=4>';
		push(@cols, "${timage}${sb}".$attr{'TOPORT'}."${se}" );
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
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
