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

my $timegroup = $in{'timegroup'};
my $newtimegroup = $in{'newtimegroup'};
my @items = split(/\0/, $in{'items'});
my $description = $in{'description'};

if( ! $fw->checkName($newtimegroup) ) { &error( $text{save_timegroup_error6} ); }

if( $in{'delete'} ) {
	# delete timegroup
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $timegroup = $d;
			$whatfailed = $text{save_timegroup_error_title1};
			if( !$fw->DeleteTimeGroup($timegroup) ) { &error( $text{save_timegroup_error1} ); }
		}
	} elsif( $timegroup ne '' ) {
		$whatfailed = $text{save_timegroup_error_title1};
		if( !$fw->DeleteTimeGroup($timegroup) ) { &error( $text{save_timegroup_error1} ); }
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_timegroup_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $timegroup ) {
				&error( $text{save_timegroup_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_timegroup_error_title3};
	}
	if ( $timegroup eq '' ) { &error( $text{save_timegroup_error3} ); }
	if ( $timegroup eq 'always' ) { &error( $text{save_timegroup_error7} ); }

	if( $#items < 0 ) { &error( $text{save_timegroup_error4} ); }
	$fw->AddTimeGroup( $timegroup, $description, @items );
	if( !$in{'new'} && $newtimegroup ne $timegroup ) {
		if( !$fw->RenameItem( $timegroup, $newtimegroup ) ) {
			&error( text('save_timegroup_error5', $timegroup, $newtimegroup) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
