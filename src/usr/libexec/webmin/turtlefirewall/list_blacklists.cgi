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

&ui_print_header( $text{'list_blacklists_title'}, $text{'title'}, "" );

showBlackLists();
print "<br><br>";

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showBlackLists {
	@tds = ( "width=1% align=center valign=center", "width=20%", "width=20%", "width=20%", "width=1% align=center valign=center" );
	print &ui_columns_start([ "<b>$text{'items'}</b>",
				  "<b>$text{'name'}</b>",
		       		  "<b>$text{'description'}</b>",
		       		  "<b>$text{'location'}</b>",
		       		  "<b>$text{'autoupdate'}</b>" ], 100, 0, \@tds);
        my @items = ();
        foreach my $b (sort keys %blacklists) {
		local @cols;
		my $blacklistcount = qx{wc -l < $blacklists{$b}{LOCATION} 2>/dev/null};
		if( $blacklistcount eq '' ) { $blacklistcount = '0'; }
		my $sb = $fw->GetOption($b) ne 'on' ? '<strike><font color=grey>' : '';	# StrikeBegin
		my $se = $fw->GetOption($b) ne 'on' ? '</strike></font>' : '';		# StrikeEnd
		push(@cols, "${sb}".$blacklistcount."${se}");
		push(@cols, "${sb}".$b."${se}");
		push(@cols, "${sb}".$blacklists{$b}{DESCRIPTION}."${se}");
		push(@cols, "${sb}".$blacklists{$b}{LOCATION}."${se}");
		my $autoupdate = 'NO';
		if( -e $blacklists{$b}{CRON} ) { $autoupdate = 'YES'; }
 		if( $autoupdate eq 'YES' ) {
			my $cb = $sb eq '' ? '<font color=green>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';		# ColourEnd
			push(@cols, "${sb}${cb}".$autoupdate."${ce}${se}");
		} else {
			my $cb = $sb eq '' ? '<font color=red>' : '';	# ColourBegin
			my $ce = $se eq '' ? '</font>' : '';		# ColourEnd
			push(@cols, "${sb}${cb}".$autoupdate."${ce}${se}");
		}
	        print &ui_columns_row(\@cols, \@tds);
        }
	print &ui_columns_end();
}
