#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();

my $idx = $in{'idx'};
my $newIdx = $in{'newIdx'};
my $virtual = $in{'virtual'};
my $real = $in{'real'};
my ($service, $port) = &formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
if( $service eq '' ) { $service = 'all'; }
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
                &error( $text{save_nat_error1} );
        }

	if( $port ne '' ) {
		my @ports = split( /:/, $port, 2 );
		foreach my $p (@ports) {
			# ensure integer
			$p = $p + 0;
			if( $p < 1 || $p > 65535 ) {
				&error( $text{save_nat_error2} );
			}
		}
		$port = join(":", @ports);
	}

	if( $toport ne '' ) {
		# ensure integer
		$toport = $toport + 0;
		if( $toport < 1 || $toport > 65535 ) {
			&error( $text{save_nat_error3} );
		}
		if( $service ne 'tcp' && $service ne 'udp' ) {
			&error( $text{save_nat_error4} );
		}
	}

        if( $in{'new'} ) {
                $fw->AddNat( 0, $virtual, $real, $service, $port, $toport, $active );
        } else {
                $fw->AddNat( $idx, $virtual, $real, $service, $port, $toport, $active );
        }
}

if( $idx ne $newIdx ) { $fw->MoveNat( $idx, $newIdx ); $idx=$newIdx; }
$fw->SaveFirewall();
&redirect( 'list_nat.cgi'.($in{'delete'} ? '' : "?table=nat&idx=$idx") );
