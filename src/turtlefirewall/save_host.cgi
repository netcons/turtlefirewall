#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

my $host = $in{'host'};
my $newhost = $in{'newhost'};
my $ip = $in{'ip'};
my $mac = $in{'mac'};
my $zone = $in{'zone'};
my $description = $in{'description'};

if( ! $fw->checkName($newhost) ) {
	error( $text{save_host_error8} );
}

if( $in{'delete'} ) {
	# delete host
	$whatfailed = $text{save_host_error_title1};
	if( !$fw->DeleteHost($host) ) {
		error( $text{save_host_error1} );
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_host_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $host ) {
				error( $text{save_host_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_host_error_title3};
	}
	if ( $host eq '' ) { error( $text{save_host_error3} ); }
	if ( ! $fw->GetZone($zone) ) { error( $text{save_host_error4} ); }
	if ( $ip !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/ ) { error( $text{save_host_error5} ); }
	if ( $mac ne '' && $mac !~ /^[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}$/ ) {
		error( $text{save_host_error6} );
	}
	$fw->AddHost($host, $ip, $mac, $zone, $description);
	if( !$in{'new'} && $newhost ne $host ) {
		if( !$fw->RenameItem( $host, $newhost ) ) {
			error( text('save_host_error7', $host, $newhost) );
		}
	}
}

$fw->SaveFirewall();
redirect( 'list_items.cgi' );
