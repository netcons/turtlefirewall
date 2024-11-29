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
my $newIdx = $in{'newIdx'};
my $src = $in{'src'};
my $dst = $in{'dst'};
my ($service, $port) = &formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
my $is_masquerade = $in{'masquerade'};
my $active = $in{'active'};

if( $in{'delete'} ) {
	# delete masquerade
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $idx = $d;
			$whatfailed = $text{save_masq_error_title1};
			$fw->DeleteMasquerade($idx);
		}
	} elsif( $idx ne '' ) {
		$whatfailed = $text{save_masq_error_title1};
		$fw->DeleteMasquerade($idx);
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_masq_error_title2};
	} else {
		$whatfailed = $text{save_masq_error_title3};
	}
	
	if( $port ne '' ) {
		my @ports = split( /:/, $port, 2 );
		foreach my $p (@ports) {
			# ensure integer
			$p = $p + 0;
			if( $p < 1 || $p > 65535 ) {
				&error( $text{save_masq_error1} );
			}
		}
		$port = join(":", @ports);
	}

	if( $port ne '' && $service ne 'tcp' && $service ne 'udp' ) {
		&error( $text{save_masq_error2} );
	}
	
	$fw->AddMasquerade( $in{'new'} ? 0 : $idx, $src, $dst, $service, $port, $is_masquerade, $active );
}

if( $idx ne $newIdx ) { $fw->MoveMasquerade( $idx, $newIdx ); $idx=$newIdx; }
$fw->SaveFirewall();
&redirect( 'list_nat.cgi'.($in{'delete'} ? '' : "?table=masquerade&idx=$idx") );
