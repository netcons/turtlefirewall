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
my $src = $in{'src'};
my $dst = $in{'dst'};
my $service = $in{'service'};
my $port = $in{'port'};
my $helper = $in{'helper'};
my $active = $in{'active'};

if( $in{'delete'} ) {
	# delete rule
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $idx = $d;
			$whatfailed = $text{save_conntrack_error_title1};
			$fw->DeleteConntrack($idx);
		}
	} elsif( $idx ne '' ) {
		$whatfailed = $text{save_conntrack_error_title1};
		$fw->DeleteConntrack($idx);
	}
} else {
	$whatfailed = $in{'new'} ? $text{save_conntrack_error_title2} : $text{save_conntrack_error_title3};

	if( $port ne '' ) {
		my @ports = split( /:/, $port, 2 );
		foreach my $p (@ports) {
			# ensure integer
			$p = $p + 0;
			if( $p < 1 || $p > 65535 ) {
				error( $text{save_conntrack_error1} );
			}
		}
		$port = join(":", @ports);
	}

	if( $src eq '' || $dst eq '' ) {
		error( $text{save_conntrack_error2} );
	}

	if( $helper eq 'ftp' && $service ne 'tcp' ) {
		error( $text{save_conntrack_error3} );
	}

	if( $helper eq 'tftp' && $service ne 'udp' ) {
		error( $text{save_conntrack_error4} );
	}

	if( $helper eq 'pptp' && $service ne 'tcp' ) {
		error( $text{save_conntrack_error5} );
	}

	if( $helper eq 'RAS' && $service ne 'udp' ) {
		error( $text{save_conntrack_error6} );
	}

	if( $helper eq 'Q.931' && $service ne 'tcp' ) {
		error( $text{save_conntrack_error7} );
	}

	if( $helper eq 'amanda' && $service ne 'udp' ) {
		error( $text{save_conntrack_error8} );
	}

	if( $helper eq 'irc' && $service ne 'tcp' ) {
		error( $text{save_conntrack_error9} );
	}

	if( $helper eq 'sane' && $service ne 'tcp' ) {
		error( $text{save_conntrack_error10} );
	}

	if( $helper eq 'snmp' && $service ne 'udp' ) {
		error( $text{save_conntrack_error11} );
	}

	if( $helper eq 'netbios-ns' && $service ne 'udp' ) {
		error( $text{save_conntrack_error12} );
	}

	$fw->AddConntrack( $in{'new'} ? 0 : $idx, $src, $dst, $service, $port, $helper, $active );
}

$fw->SaveFirewall();
redirect( 'list_rawrules.cgi'.($in{'delete'} ? "?idx=$idx" : '') );
