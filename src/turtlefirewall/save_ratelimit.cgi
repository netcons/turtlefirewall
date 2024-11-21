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

my $ratelimit = $in{'ratelimit'};
my $newratelimit = $in{'newratelimit'};
my $rate = $in{'rate'};
my $description = $in{'description'};

if( ! $fw->checkName($newratelimit) ) { &error( $text{save_ratelimit_error6} ); }

if ( $ratelimit eq 'none' || $newratelimit eq 'none' ) { &error( $text{save_ratelimit_error7} ); }

if( $in{'delete'} ) {
	# delete ratelimit
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $ratelimit = $d;
			$whatfailed = $text{save_ratelimit_error_title1};
			if( !$fw->DeleteRateLimit($ratelimit) ) { &error( $text{save_ratelimit_error1} ); }
		}
	} elsif( $ratelimit ne '' ) {
		$whatfailed = $text{save_ratelimit_error_title1};
		if( !$fw->DeleteRateLimit($ratelimit) ) { &error( $text{save_ratelimit_error1} ); }
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_ratelimit_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $ratelimit ) {
				&error( $text{save_ratelimit_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_ratelimit_error_title3};
	}
	if ( $ratelimit eq '' ) { &error( $text{save_ratelimit_error3} ); }

	if( $rate eq '' || ($rate < 0.1 || $rate > 999) ) {
		&error( $text{save_ratelimit_error4} );
	}

	$fw->AddRateLimit( $ratelimit, $rate, $description );
	if( !$in{'new'} && $newratelimit ne $ratelimit ) {
		if( !$fw->RenameItem( $ratelimit, $newratelimit ) ) {
			&error( &text('save_ratelimit_error5', $ratelimit, $newratelimit) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
