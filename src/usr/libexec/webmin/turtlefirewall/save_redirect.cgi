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
my $src = $in{'src'};
my $dst = $in{'dst'};
my ($service, $port) = formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
my $toport = $in{'toport'};
my $is_redirect = $in{'redirect'};
my $active = $in{'active'};

if( $in{'delete'} ) {
	# delete redirect
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $idx = $d;
			$whatfailed = $text{save_redirect_error_title1};
			$fw->DeleteRedirect($idx);
		}
	} elsif( $idx ne '' ) {
		$whatfailed = $text{save_redirect_error_title1};
		$fw->DeleteRedirect($idx);
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_redirect_error_title2};
	} else {
		$whatfailed = $text{save_redirect_error_title3};
	}

	if( $port ne '' && ($port < 0 || $port > 65535) ) {
		error( $text{save_redirect_error1} );
	}

	if( $port ne '' && $service ne 'tcp' && $service ne 'udp' ) {
		error( $text{save_redirect_error2} );
	}

	$fw->AddRedirect( $in{'new'} ? 0 : $idx, $src, $dst, $service, $port, $toport, $is_redirect, $active );
}

$fw->SaveFirewall();
redirect( 'list_nat.cgi' );
