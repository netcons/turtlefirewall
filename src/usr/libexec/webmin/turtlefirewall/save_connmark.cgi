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
my ($service, $port) = formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
my ($ndpi, $category) = formNdpiProtocolParse( $in{'ndpiprotocoltype'}, $in{'ndpiprotocol2'}, $in{'category'} );
my $set = $in{'set'};
if( $set eq 'any' ) { $set = ''; }
my $time = $in{'time'};
if( $time eq 'always' ) { $time = ''; }
my $mark = $in{'mark'};
my $active = $in{'active'};

if( $in{'delete'} ) {
	# delete rule
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $idx = $d;
			$whatfailed = $text{save_connmark_error_title1};
			$fw->DeleteConnmark($idx);
		}
	} elsif( $idx ne '' ) {
		$whatfailed = $text{save_connmark_error_title1};
		$fw->DeleteConnmark($idx);
	}
} else {
	$whatfailed = $in{'new'} ? $text{save_connmark_error_title2} : $text{save_connmark_error_title3};

	if( $port ne '' && ($port < 0 || $port > 65535) ) {
		error( $text{save_connmark_error1} );
	}

	if( $port ne '' && $service ne 'tcp' && $service ne 'udp' ) {
		error( $text{save_connmark_error2} );
	}

	if( $src eq '' || $dst eq '' ) {
		error( $text{save_connmark_error3} );
	}

	if( $mark !~ /^(0x[A-Fa-f0-9]+|[0-9]+)$/ ) {
		error( $text{save_connmark_error4} );
	}

	$fw->AddConnmark( $in{'new'} ? 0 : $idx, $src, $dst, $service, $ndpi, $category, $set, $port, $time, $mark, $active );
}

$fw->SaveFirewall();
redirect( 'list_manglerules.cgi'.($in{'delete'} ? "?idx=$idx" : '') );
