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

my $time = $in{'time'};
my $newtime = $in{'newtime'};
my $timestart = $in{'timestart'};
my $timestop = $in{'timestop'};
my $description = $in{'description'};

if( ! $fw->checkName($newtime) ) { &error( $text{save_time_error8} ); }

if ( $time eq 'always' || $newtime eq 'always' ) { &error( $text{save_time_error9} ); }

if( $in{'delete'} ) {
	# delete time
        if( $in{'d'} ) {
                @d = split(/\0/, $in{'d'});
                foreach $d (sort { $b <=> $a } @d) {
                        my $time = $d;
                        $whatfailed = $text{save_time_error_title1};
                        if( !$fw->DeleteTime($time) ) { &error( $text{save_time_error1} ); }
                }
        } elsif( $time ne '' ) {
                $whatfailed = $text{save_time_error_title1};
                if( !$fw->DeleteTime($time) ) { &error( $text{save_time_error1} ); }
        }
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_time_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $time ) {
				&error( $text{save_time_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_time_error_title3};
	}
	if ( $time eq '' ) { &error( $text{save_time_error3} ); }
	if ( $timestart eq '' || $timestop eq '' ) { &error( $text{save_time_error5} ); }
	if ( $timestart ne '' && $timestart !~ /^([0-1][0-9]|[2][0-3]):([0-5][0-9])$/ ) {
		&error( $text{save_time_error6} );
	}
	if ( $timestop ne '' && $timestop !~ /^([0-1][0-9]|[2][0-3]):([0-5][0-9])$/ ) {
		&error( $text{save_time_error6} );
	}

        my @items = ();
        foreach my $k (keys %in) {
                if( $k =~ /^item_(.*)$/ ) {
                        push @items, $1;
                }
	}

	if( $#items < 0 ) { &error( $text{save_time_error4} ); }
	$weekdays = join(",", @items);
	$fw->AddTime($time, $weekdays, $timestart, $timestop, $description);
	if( !$in{'new'} && $newtime ne $time ) {
		if( !$fw->RenameItem( $time, $newtime ) ) {
			&error( &text('save_time_error6', $time, $newtime) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
