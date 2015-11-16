#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

&header( $text{list_nat_title}, '' );

showNat();
showMasquerade();
showRedirect();

print "<br><br>";
&footer('','turtle firewall index');


#============================================================================

sub showNat {
	print "<br><big><b>$text{nat}</b></big>
		<table border width=\"100%\">
			<tr $tb>
				<th width=\"5%\">#</th>
				<th width=\"30%\">$text{virtual_host}</th>
				<th width=\"30%\">$text{real_host}</th>
				<th width=\"20%\">$text{nat_service}</th>
				<th width=\"10%\">$text{nat_port}</th>
				<th width=\"5%\">$text{nat_active}</th>
				<th>&nbsp;</th>
			</tr>";
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
		my $href = "\"edit_nat.cgi?idx=$i\"";
		print "<tr $cb>";
		print "<td align=\"center\"><a href=$href>$i</a></td>";
		print "<td><a href=$href>".$attr{'VIRTUAL'};
		my %zone = $fw->GetZone($attr{'VIRTUAL'});
		if( $zone{IF} ne '' ) {
			print ' ('.$zone{IF}.')';
		}
		print "</a></td>";
		print "<td><a href=$href>".$attr{'REAL'}."</a></td>";
		$attr{'SERVICE'} =~ s/,/, /g;
		print "<td align=\"center\"><a href=$href>".($attr{'SERVICE'} ne '' ? $attr{'SERVICE'} : '&nbsp;')."</a></td>";
		print "<td align=\"center\"><a href=$href>".($attr{'PORT'} ne '' ? $attr{'PORT'} : '&nbsp;')."</a></td>";
		print "<td align=\"center\"><a href=$href>";
		if( $attr{'ACTIVE'} eq 'NO' ) {
			print '<font color="red">'.$text{NO}.'</font>';
		} else {
			print $text{YES};
		}
		print "</a></td>";

		print '<td width="1%" valign="top">
			<table cellspacing="0" cellpadding="0"><tr>';
				if( $i < $nNat ) {
					print qq~<td width="50%"><a href="list_nat.cgi?table=nat&idx=$i&down=1"><img src="images/down.gif" border="0" hspace="1" vspace="0" alt="down"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;&nbsp;&nbsp;"></td>';
				}
				if( $i > 1 ) {
					print qq~<td width="50%"><a href="list_nat.cgi?table=nat&idx=$i&up=1"><img src="images/up.gif" border="0" hspace="1" vspace="0" alt="up"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;"></td>';
				}
		print ' </tr></table>
			</td>';

		print "</tr>";
	}
	print "</table>\n";
	print '<a href="edit_nat.cgi?new=1">'.$text{list_nat_create_nat}.'</a><br>';
}

sub showMasquerade {
	print "<br><big><b>$text{masquerade}</b></big>
		<table border width=\"100%\">
			<tr $tb>
				<th width=\"5%\">#</th>
				<th width=\"30%\">$text{masq_src}</th>
				<th width=\"30%\">$text{masq_dst}</th>
				<th width=\"20%\">$text{masq_service}</th>
				<th width=\"5%\">$text{masq_port}</th>
				<th width=\"5%\">$text{masq_masquerade}</th>
				<th width=\"5%\">$text{masq_active}</th>
				<th width=\"5%\">&nbsp;</th>
			</tr>";
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
		my $href = "\"edit_masq.cgi?idx=$i\"";
		print "<tr $cb>";
		print "<td align=\"center\"><a href=$href>$i</a></td>";
		
		print "<td align=\"left\"><a href=$href>".($attr{'SRC'} ne '' ? $attr{'SRC'} : '*')."</a></td>";
		print "<td align=\"left\"><a href=$href>".($attr{'DST'} ne '' ? $attr{'DST'} : '&nbsp;')."</a></td>";		
		$attr{'SERVICE'} =~ s/,/, /g;
		print "<td align=\"center\"><a href=$href>".($attr{'SERVICE'} ne '' ? $attr{'SERVICE'} : '&nbsp;')."</a></td>";
		print "<td align=\"center\"><a href=$href>".($attr{'PORT'} ne '' ? $attr{'PORT'} : '&nbsp;')."</a></td>";		
		print "<td align=\"center\"><a href=$href>";
		if( $attr{'MASQUERADE'} eq 'NO' ) {
			print '<font color="red">'.$text{NO}.'</font>';
		} else {
			print $text{YES};
		}
		print "</a></td>";
		print "<td align=\"center\"><a href=$href>";
		if( $attr{'ACTIVE'} eq 'NO' ) {
			print '<font color="red">'.$text{NO}.'</font>';
		} else {
			print $text{YES};
		}
		print "</a></td>";
		
		print '<td width="1%" valign="top">
			<table cellspacing="0" cellpadding="0"><tr>';
				if( $i < $nMasq ) {
					print qq~<td width="50%"><a href="list_nat.cgi?table=masquerade&idx=$i&down=1"><img src="images/down.gif" border="0" hspace="1" vspace="0" alt="down"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;&nbsp;&nbsp;"></td>';
				}
				if( $i > 1 ) {
					print qq~<td width="50%"><a href="list_nat.cgi?table=masquerade&idx=$i&up=1"><img src="images/up.gif" border="0" hspace="1" vspace="0" alt="up"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;"></td>';
				}
		print ' </tr></table>
			</td>';		
		
		print "</tr>";
	}
	print "</table>\n";
	print '<a href="edit_masq.cgi?new=1">'.$text{list_nat_create_masq}.'</a><br>';
}

sub showRedirect {
	print "<br><big><b>$text{redirect}</b></big>
		<table border width=\"100%\">
			<tr $tb>
				<th width=\"5%\">#</th>
				<th width=\"30%\">$text{redirect_src}</th>
				<th width=\"30%\">$text{redirect_dst}</th>
				<th width=\"10%\">$text{redirect_service}</th>
				<th width=\"5%\">$text{redirect_port}</th>
				<th width=\"5%\">$text{redirect_redirect}</th>
				<th width=\"10%\">$text{redirect_toport}</th>
				<th width=\"5%\">$text{redirect_active}</th>
				<th>&nbsp;</th>
			</tr>";

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
		my $href = "\"edit_redirect.cgi?idx=$i\"";
		print "<tr $cb>";
		print "<td align=\"center\"><a href=$href>$i</a></td>";
		print "<td><a href=$href>".$attr{'SRC'}."</a></td>";
		print "<td><a href=$href>".$attr{'DST'}."</a></td>";
		print "<td align=\"center\"><a href=$href>".$attr{'SERVICE'}."</a></td>";
		print "<td align=\"center\"><a href=$href>".$attr{'PORT'}."</a></td>";
		print "<td align=\"center\"><a href=$href>";
		if( $attr{'REDIRECT'} eq 'NO' ) {
			print '<font color="red">'.$text{NO}.'</font>';
		} else {
			print $text{YES};
		}
		print "</a></td>";
		print "<td align=\"center\"><a href=$href>".$attr{'TOPORT'}."</a></td>";
		print "<td align=\"center\"><a href=$href>";
		if( $attr{'ACTIVE'} eq 'NO' ) {
			print '<font color="red">'.$text{NO}.'</font>';
		} else {
			print $text{YES};
		}
		print "</a></td>";

		print '<td width="1%" valign="top">
			<table cellspacing="0" cellpadding="0"><tr>';
				if( $i < $nRedirect ) {
					print qq~<td width="50%"><a href="list_nat.cgi?table=redirect&idx=$i&down=1"><img src="images/down.gif" border="0" hspace="1" vspace="0" alt="down"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;&nbsp;&nbsp;"></td>';
				}
				if( $i > 1 ) {
					print qq~<td width="50%"><a href="list_nat.cgi?table=redirect&idx=$i&up=1"><img src="images/up.gif" border="0" hspace="1" vspace="0" alt="up"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;"></td>';
				}
		print ' </tr></table>
			</td>';

		print "</tr>";
	}
	print "</table>\n";
	print '<a href="edit_redirect.cgi?new=1">'.$text{list_nat_create_redirect}.'</a><br>';
}
