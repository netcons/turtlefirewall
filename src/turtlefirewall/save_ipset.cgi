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

my $ipset = $in{'ipset'};
my $newipset = $in{'newipset'};
my $ip = $in{'ip'};
my $type = $in{'type'};
my $zone = $in{'zone'};
my $description = $in{'description'};

if( ! $fw->checkName($newipset) ) { &error( $text{save_ipset_error8} ); }

if( $in{'delete'} ) {
	# delete ipset
        if( $in{'d'} ) {
                @d = split(/\0/, $in{'d'});
                foreach $d (sort { $b <=> $a } @d) {
                        my $ipset = $d;
                        $whatfailed = $text{save_ipset_error_title1};
                        if( !$fw->DeleteIPSet($ipset) ) { &error( $text{save_ipset_error1} ); }
                }
        } elsif( $ipset ne '' ) {
                $whatfailed = $text{save_ipset_error_title1};
                if( !$fw->DeleteIPSet($ipset) ) { &error( $text{save_ipset_error1} ); }
        }
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_ipset_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $ipset ) {
				&error( $text{save_ipset_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_ipset_error_title3};
	}
	if ( $ipset eq '' ) { &error( $text{save_ipset_error3} ); }
	if ( ! $fw->GetZone($zone) ) { &error( $text{save_ipset_error4} ); }
	if ( $ip eq 'ip_blacklist' ) { &error( $text{save_ipset_error5} ); }
	if ( $ip eq '' ) { &error( $text{save_ipset_error6} ); }
	$fw->AddIPSet( $ipset, $ip, $type, $zone, $description );
	if( !$in{'new'} && $newipset ne $ipset ) {
		if( !$fw->RenameItem( $ipset, $newipset ) ) {
			&error( &text('save_ipset_error7', $ipset, $newipset) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
