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
$src =~ s/\0/,/g;
my $dst = $in{'dst'};
$dst =~ s/\0/,/g;
my ($service, $port) = &formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
if( $service eq '' ) { $service = 'all'; }
my ($ndpi, $category) = &formNdpiProtocolParse( $in{'ndpiprotocoltype'}, $in{'ndpiprotocol2'}, $in{'category'} );
my $hostnameset = $in{'hostnameset'};
if( $hostnameset eq 'any' ) { $hostnameset = ''; }
my $riskset = $in{'riskset'};
if( $riskset eq 'none' ) { $riskset = ''; }
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

	if( $port ne '' ) {
		my @ports = split( /:/, $port, 2 );
		foreach my $p (@ports) {
			# ensure integer
			$p = $p + 0;
			if( $p < 1 || $p > 65535 ) {
				&error( $text{save_connmark_error1} );
			}
		}
		$port = join(":", @ports);
	}

	if( $port ne '' && $service ne 'tcp' && $service ne 'udp' ) {
		&error( $text{save_connmark_error2} );
	}

	if( $src eq '' || $dst eq '' ) {
		&error( $text{save_connmark_error3} );
	}

	if( $mark !~ /^(0x[A-Fa-f0-9]+|[0-9]+)$/ ) {
		&error( $text{save_connmark_error4} );
	}

	$fw->AddConnmark( $in{'new'} ? 0 : $idx, $src, $dst, $service, $ndpi, $category, $hostnameset, $riskset, $port, $time, $mark, $active );
}

if( $idx ne $newIdx ) { $fw->MoveConnmark( $idx, $newIdx ); $idx=$newIdx; }
$fw->SaveFirewall();
&redirect( 'list_manglerules.cgi'.($in{'delete'} ? '' : "?table=connmark&idx=$idx") );
