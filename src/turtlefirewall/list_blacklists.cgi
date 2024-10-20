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

&ui_print_header( "<img src=images/blacklist.png hspace=4>$text{'list_blacklists_title'}", $text{'title'}, "" );

&showBlackLists();
print "<br><br>";

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showBlackLists {
	@tds = ( "width=20%", "width=20%", "width=20%", "width=1% style=text-align:center", "width=1% style=text-align:center" );
	print &ui_columns_start([ "<b>$text{'name'}</b>",
		       		  "<b>$text{'description'}</b>",
		       		  "<b>$text{'location'}</b>",
		       		  "<b>$text{'items'}</b>",
		       		  "<b>$text{'autoupdate'}</b>" ], 100, 0, \@tds);
        my @items = ();
        foreach my $b (sort keys %blacklists) {
		local @cols;
		push(@cols, "<img src=images/blacklist.png hspace=4>$b");
		push(@cols, "<img src=images/info.png hspace=4>$blacklists{$b}{DESCRIPTION}");
		push(@cols, "<img src=images/address.png hspace=4>$blacklists{$b}{LOCATION}");
		my $blacklistcount = qx{wc -l < $blacklists{$b}{LOCATION} 2>/dev/null};
		if( $blacklistcount eq '' ) { $blacklistcount = '0'; }
		push(@cols, $blacklistcount);
		my $autoupdate = 'NO';
		if( -e $blacklists{$b}{CRON} ) { $autoupdate = 'YES'; }
		my $aimage = $autoupdate eq 'YES' ? '<img src=images/yes.png hspace=4>' : '<img src=images/no.png hspace=4>';
		my $cb = $autoupdate eq 'YES' ? '<span style=color:green>' : '<span style=color:red>';	# ColourBegin
		my $ce = '</span>';								# ColourEnd
		push(@cols, "${aimage}${cb}${autoupdate}${ce}");
	        print &ui_columns_row(\@cols, \@tds);
        }
	print &ui_columns_end();
}
