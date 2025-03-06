#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
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
my $ratelimit = $in{'ratelimit'};
if( $ratelimit eq 'none' ) { $ratelimit = ''; }
my $time = $in{'time'};
if( $time eq 'always' ) { $time = ''; }
my $target = $in{'target'};
my $active = $in{'active'};
my $log = $in{'log'};
my $description = $in{'description'};

if( $in{'delete'} ) {
	# delete rule
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $idx = $d;
			$whatfailed = $text{save_rule_error_title1};
			$fw->DeleteRule($idx);
		}
	} elsif( $idx ne '' ) {
		$whatfailed = $text{save_rule_error_title1};
		$fw->DeleteRule($idx);
	}
} else {
	$whatfailed = $in{'new'} ? $text{save_rule_error_title2} : $text{save_rule_error_title3};

	if( $port ne '' ) {
		my @ports = split( /:/, $port, 2 );
		foreach my $p (@ports) {
			# ensure integer
			$p = $p + 0;
			if( $p < 1 || $p > 65535 ) {
				&error( $text{save_rule_error1} );
			}
		}
		$port = join(":", @ports);
	}

	if( $port ne '' && $service ne 'tcp' && $service ne 'udp' ) {
		&error( $text{save_rule_error2} );
	}

	if( $src eq 'FIREWALL' && $dst eq 'FIREWALL' ) {
		&error( $text{save_rule_error3} );
	}

	if( $src eq '' || $dst eq '' ) {
		&error( $text{save_rule_error4} );
	}

	if( $target ne 'DROP' && $ratelimit ne '' ) {
		&error( $text{save_rule_error5} );
	}

	if( $log ne '' && $ratelimit ne '' ) {
		&error( $text{save_rule_error6} );
	}

	$fw->AddRule( $in{'new'} ? 0 : $idx, $src, $dst, $service, $ndpi, $category, $hostnameset, $riskset, $ratelimit, $port, $time, $target, $active, $log, $description );
}

if( $idx ne $newIdx ) { $fw->MoveRule( $idx, $newIdx ); $idx=$newIdx; }
$fw->SaveFirewall();
&redirect( 'list_rules.cgi'.($in{'delete'} ? '' : "?idx=$idx") );
