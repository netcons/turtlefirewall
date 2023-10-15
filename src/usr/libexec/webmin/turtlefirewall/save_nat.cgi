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

	if( $port ne '' && $port !~ /^(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[0-9]{1,4})$|^(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[0-9]{1,4}):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[0-9]{1,4})$/ ) {
                error( $text{save_nat_error2} );
	}

	if( $toport ne '' ) {
		if( $toport !~ /^()([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])$/ ) {
			error( $text{save_nat_error3} );
		}
		if( $service ne 'tcp' && $service ne 'udp' ) {
			error( $text{save_nat_error4} );
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
