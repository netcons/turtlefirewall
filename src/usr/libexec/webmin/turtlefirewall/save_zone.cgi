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

$newzone = $in{'newzone'};
$zone = $in{'zone'};
$if = $in{'if'};
$description = $in{'description'};

if( ! $fw->checkName($newzone) ) { error( $text{save_zone_error8} ); }
if( ! $fw->checkName($description) ) { error( $text{save_zone_error9} ); }

# A zone to add
if( $in{'delete'} ) {
	# delete zone
        if( $in{'d'} ) {
                @d = split(/\0/, $in{'d'});
                foreach $d (sort { $b <=> $a } @d) {
                        my $zone = $d;
                        $whatfailed = $text{save_zone_error_title1};
                        if( !$fw->DeleteZone($zone) ) { error( $text{save_zone_error1} ); }
                }
        } elsif( $zone ne '' ) {
                $whatfailed = $text{save_zone_error_title1};
                if( !$fw->DeleteZone($zone) ) { error( $text{save_zone_error1} ); }
        }
} else {
	$whatfailed = $in{'new'} ? $text{save_zone_error_title2} : $text{save_zone_error_title3};
	if ( $if eq '' ) { error( $text{save_zone_error2} ); }
	if ( $if =~ /\:/ ) { error( $text{save_zone_error3} ); }
	if( $in{'new'} ) {
		# create zone
		if ( $zone eq '' ) { error( $text{save_zone_error4} ); }
		if ( $zone eq 'FIREWALL' ) { error( $text{save_zone_error5} ); }
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $zone ) {
				error( $text{save_zone_error6} );
			}
		}
		if( ! $fw->checkName($zone) ) { error( $text{save_zone_error8} ); }
		$fw->AddZone( $zone, $if, $description );
	} else {
		# save zone
		$fw->AddZone( $zone, $if, $description );
		if( $newzone ne $zone ) {
			if( !$fw->RenameItem( $zone, $newzone ) ) {
				error( text('save_zone_error7', $zone, $newzone) );
			}
		}
	}
}

# &header( $text{'title'}, '' );

$fw->SaveFirewall();
redirect( 'list_items.cgi' );
