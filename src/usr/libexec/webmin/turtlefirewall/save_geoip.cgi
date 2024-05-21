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

my $geoip = $in{'geoip'};
my $newgeoip = $in{'newgeoip'};
my $ip = $in{'ip'};
my $zone = $in{'zone'};
my $description = $in{'description'};

if( ! $fw->checkName($newgeoip) ) { &error( $text{save_geoip_error7} ); }

if( $in{'delete'} ) {
	# delete geoip
        if( $in{'d'} ) {
                @d = split(/\0/, $in{'d'});
                foreach $d (sort { $b <=> $a } @d) {
                        my $geoip = $d;
                        $whatfailed = $text{save_geoip_error_title1};
                        if( !$fw->DeleteGeoip($geoip) ) { &error( $text{save_geoip_error1} ); }
                }
        } elsif( $geoip ne '' ) {
                $whatfailed = $text{save_geoip_error_title1};
                if( !$fw->DeleteGeoip($geoip) ) { &error( $text{save_geoip_error1} ); }
        }
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_geoip_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $geoip ) {
				&error( $text{save_geoip_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_geoip_error_title3};
	}
	if ( $geoip eq '' ) { &error( $text{save_geoip_error3} ); }
	if ( ! $fw->GetZone($zone) ) { &error( $text{save_geoip_error4} ); }
	if ( $ip !~ /^[A-Z1-2]{2}$/ ) { &error( $text{save_geoip_error5} ); }
	$fw->AddGeoip( $geoip, $ip, $zone, $description );
	if( !$in{'new'} && $newgeoip ne $geoip ) {
		if( !$fw->RenameItem( $geoip, $newgeoip ) ) {
			&error( $text('save_geoip_error6', $geoip, $newgeoip) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
