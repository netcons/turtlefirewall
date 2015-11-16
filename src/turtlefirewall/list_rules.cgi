#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

&header( $text{list_rules_title}, '' );

showRule();

print "<br><br>";
&footer('','turtle firewall index');


#============================================================================

sub showRule {

	print "<br>
		<table border width=\"100%\">
			<tr $tb>
				<th>#</th>
				<th>$text{rule_src}</th>
				<th>$text{rule_dst}</th>
				<th>$text{rule_service}</th>
				<th>$text{rule_port}</th>
				<th>$text{rule_target}</th>
				<th>$text{rule_mark}</th>
				<th>$text{rule_active}</th>
				<th>$text{description}</th>
				<th>&nbsp;</th>
			</tr>";
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

		if( $attr{'TARGET'} eq '' ) { $attr{'TARGET'} = 'ACCEPT'; }

		my $bb = $idx == $i ? '<b>' : '';	# BoldBegin
		my $be = $idx == $i ? '</b>' : '';	# BoldEnd

		my $href = "\"edit_rule.cgi?idx=$i\"";
		print "<tr $cb>";
		print "<td align=\"center\" valign=\"top\"><a href=$href>${bb}$i${be}</a></td>";
		$attr{'SRC'} =~ s/,/, /g;
		print "<td valign=\"top\"><a href=$href>${bb}".$attr{'SRC'}."${be}</a></td>";
		$attr{'DST'} =~ s/,/, /g;
		print "<td valign=\"top\"><a href=$href>${bb}".$attr{'DST'}."${be}</a></td>";
		$attr{'SERVICE'} =~ s/,/, /g;
		print "<td align=\"center\" valign=\"top\"><a href=$href>${bb}".$attr{'SERVICE'}."${be}</a></td>";
		print "<td align=\"center\" valign=\"top\"><a href=$href>${bb}".($attr{'PORT'} ne '' ? $attr{'PORT'} : '&nbsp;')."${be}</a></td>";

		print "<td align=\"center\" valign=\"top\"><a href=$href>${bb}";
		if( $attr{'TARGET'} ne 'ACCEPT' ) {
			print '<font color="red">'.$attr{'TARGET'}.'</font>';
		} else {
			print $attr{'TARGET'};
		}
		print "${be}</a></td>";
		print "<td align=\"center\" valign=\"top\"><a href=$href>${bb}".($attr{'MARK'} ne '' ? $attr{'MARK'} : '&nbsp;')."${be}</a></td>";

		print "<td align=\"center\" valign=\"top\"><a href=$href>${bb}";
		if( $attr{'ACTIVE'} eq 'NO' ) {
			print '<font color="red">'.$text{NO}.'</font>';
		} else {
			print $text{YES};
		}
		print "${be}</a></td>";
		print "<td valign=\"top\">${bb}".($attr{DESCRIPTION} ne '' ? $attr{DESCRIPTION} : '&nbsp;')."${be}</td>";
		print '<td width="1%" valign="top">
			<table cellspacing="0" cellpadding="0"><tr>';
				if( $i < $nRules-1 ) {
					print qq~<td width="50%"><a href="list_rules.cgi?idx=$i&down=5"><img src="images/down5.gif" border="0" hspace="1" vspace="0" alt="V"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;&nbsp;&nbsp;"></td>';
				}
				if( $i < $nRules ) {
					print qq~<td width="50%"><a href="list_rules.cgi?idx=$i&down=1"><img src="images/down.gif" border="0" hspace="1" vspace="0" alt="v"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;&nbsp;&nbsp;"></td>';
				}
				if( $i > 1 ) {
					print qq~<td width="50%"><a href="list_rules.cgi?idx=$i&up=1"><img src="images/up.gif" border="0" hspace="1" vspace="0" alt="^"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;"></td>';
				}
				if( $i > 2 ) {
					print qq~<td width="50%"><a href="list_rules.cgi?idx=$i&up=5"><img src="images/up5.gif" border="0" hspace="1" vspace="0" alt="A"></a></td>~;
				} else {
					print '<td width="50%"><img src="images/gap.gif" border="0" hspace="1" vspace="0" alt="&nbsp;&nbsp;"></td>';
				}
		print ' </tr></table>
			</td>';

		print "</tr>\n";
	}
	print "</table>\n";
	print '<a href="edit_rule.cgi?new=1">'.$text{list_rules_create_rule}.'</a><br>';
}
