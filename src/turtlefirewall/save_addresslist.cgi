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

my $addresslist = $in{'addresslist'};
my $newaddresslist = $in{'newaddresslist'};
my $location = $in{'location'};
my $type = $in{'type'};
my $description = $in{'description'};

if( ! $fw->checkName($newaddresslist) ) { &error( $text{save_addresslist_error8} ); }

if( $in{'delete'} ) {
	# delete addresslist
        if( $in{'d'} ) {
                @d = split(/\0/, $in{'d'});
                foreach $d (sort { $b <=> $a } @d) {
                        my $addresslist = $d;
                        $whatfailed = $text{save_addresslist_error_title1};
                        if( !$fw->DeleteIPSet($addresslist) ) { &error( $text{save_addresslist_error1} ); }
                }
        } elsif( $addresslist ne '' ) {
                $whatfailed = $text{save_addresslist_error_title1};
                if( !$fw->DeleteIPSet($addresslist) ) { &error( $text{save_addresslist_error1} ); }
        }
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_addresslist_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $addresslist ) {
				&error( $text{save_addresslist_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_addresslist_error_title3};
	}
	if ( $addresslist eq '' ) { &error( $text{save_addresslist_error3} ); }
	if ( $addresslist eq 'ip_blacklist' ) { &error( $text{save_addresslist_error4} ); }
	if ( $location eq '' ) { &error( $text{save_addresslist_error5} ); }
	if ( ! -f $location ) { &error( $text{save_addresslist_error6} ); }
	$fw->AddAddressList( $addresslist, $location, $type, $description );
	if( !$in{'new'} && $newaddresslist ne $addresslist ) {
		if( !$fw->RenameItem( $addresslist, $newaddresslist ) ) {
			&error( &text('save_addresslist_error7', $addresslist, $newaddresslist) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
