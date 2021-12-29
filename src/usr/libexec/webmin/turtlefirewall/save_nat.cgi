#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

my $idx = $in{'idx'};
my $virtual = $in{'virtual'};
my $real = $in{'real'};
my ($service, $port) = formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
my $toport = $in{'toport'};
my $active = $in{'active'};

# Cut interface
$virtual =~ s/ \(.*\)$//;

if( $in{'delete'} ) {
        # delete NAT
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $idx = $d;
			$whatfailed = $text{save_nat_error_title1};
			$fw->DeleteNat($idx);
		}
	} elsif( $idx ne '' ) {
		$whatfailed = $text{save_nat_error_title1};
		$fw->DeleteNat($idx);
	}
} else {
        $whatfailed = $in{'new'} ? $text{save_nat_error_title2} : $text{save_nat_error_title3};
        if( $real eq '' ) {
                error( $text{save_nat_error1} );
        }
        if( $toport ne '' ) {
		if( $service ne 'tcp' && $service ne 'udp' ) {
                	error( $text{save_nat_error2} );
		}
        }
        if( $in{'new'} ) {
                $fw->AddNat( 0, $virtual, $real, $service, $port, $toport, $active );
        } else {
                $fw->AddNat( $idx, $virtual, $real, $service, $port, $toport, $active );
        }
}

$fw->SaveFirewall();
redirect( 'list_nat.cgi' );
