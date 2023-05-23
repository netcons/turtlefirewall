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
	@tds = ( "width=10%", "width=30%", "width=30%", "width=20%", "width=10%" );
	print &ui_columns_start([ "<b>$text{'name'}</b>",
		       		  "<b>$text{'description'}</b>",
		       		  "<b>$text{'location'}</b>",
		       		  "<b>$text{'items'}</b>",
		       		  "<b>$text{'autoupdate'}</b>" ], 100, 0, \@tds);
        my @items = ();
        foreach my $b (sort keys %blacklists) {
		my $blacklistcount = qx{wc -l < $blacklists{$b}{LOCATION} 2>/dev/null};
		if( $blacklistcount eq '' ) { $blacklistcount = '0'; }
		my $autoupdate = '<font color=red>NO</font>';
		if( -e $blacklists{$b}{CRON} ) { $autoupdate = '<font color=green>YES</font>'; }
	        print &ui_columns_row([ $b, $blacklists{$b}{DESCRIPTION}, $blacklists{$b}{LOCATION}, $blacklistcount, $autoupdate ], \@tds);
        }
	print &ui_columns_end();
}
