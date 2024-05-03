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

my $net = $in{'net'};
my $newnet = $in{'newnet'};
my $ip = $in{'ip'};
my $netmask = $in{'netmask'};
my $zone = $in{'zone'};
my $description = $in{'description'};

if( ! $fw->checkName($newnet) ) { error( $text{save_net_error8} ); }
if( ! $fw->checkName($description) ) { error( $text{save_net_error9} ); }

if( $in{'delete'} ) {
	# delete net
        if( $in{'d'} ) {
                @d = split(/\0/, $in{'d'});
                foreach $d (sort { $b <=> $a } @d) {
                        my $net = $d;
                        $whatfailed = $text{save_net_error_title1};
                        if( !$fw->DeleteNet($net) ) { error( $text{save_net_error1} ); }
                }
        } elsif( $net ne '' ) {
                $whatfailed = $text{save_net_error_title1};
                if( !$fw->DeleteNet($net) ) { error( $text{save_net_error1} ); }
        }
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_net_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $net ) {
				error( $text{save_net_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_net_error_title3};
	}
	if ( $net eq '' ) { error( $text{save_net_error3} ); }
	if ( ! $fw->GetZone($zone) ) { error( $text{save_net_error4} ); }
	if ( $ip !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/ ) { error( $text{save_net_error5} ); }
	if ( $netmask !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/ ) { error( $text{save_net_error6} ); }
	$fw->AddNet( $net, $ip, $netmask, $zone, $description );
	if( !$in{'new'} && $newnet ne $net ) {
		if( !$fw->RenameItem( $net, $newnet ) ) {
			error( text('save_net_error7', $net, $newnet) );
		}
	}
}

$fw->SaveFirewall();
redirect( 'list_items.cgi' );
