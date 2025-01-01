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

my $group = $in{'group'};
my $newgroup = $in{'newgroup'};
my @items = split(/\0/, $in{'items'});
my $description = $in{'description'};

if( ! $fw->checkName($newgroup) ) { &error( $text{save_group_error6} ); }

if( $in{'delete'} ) {
	# delete group
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $group = $d;
			$whatfailed = $text{save_group_error_title1};
			if( !$fw->DeleteGroup($group) ) { &error( $text{save_group_error1} ); }
		}
	} elsif( $group ne '' ) {
		$whatfailed = $text{save_group_error_title1};
		if( !$fw->DeleteGroup($group) ) { &error( $text{save_group_error1} ); }
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_group_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $group ) {
				&error( $text{save_group_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_group_error_title3};
	}
	if ( $group eq '' ) { &error( $text{save_group_error3} ); }

	if( $#items < 0 ) { &error( $text{save_group_error4} ); }
	$fw->AddGroup( $group, $description, @items );
	if( !$in{'new'} && $newgroup ne $group ) {
		if( !$fw->RenameItem( $group, $newgroup ) ) {
			&error( &text('save_group_error5', $group, $newgroup) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
