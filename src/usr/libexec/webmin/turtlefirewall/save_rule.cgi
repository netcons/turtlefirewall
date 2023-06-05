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
$src =~ s/\0/,/g;
my $dst = $in{'dst'};
$dst =~ s/\0/,/g;
my ($service, $port) = formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
my ($ndpi, $category) = formNdpiProtocolParse( $in{'ndpiprotocoltype'}, $in{'ndpiprotocol2'}, $in{'category'} );
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

	if( $port ne '' && ($port < 0 || $port > 65535) ) {
		error( $text{save_rule_error1} );
	}

	if( $port ne '' && $service ne 'tcp' && $service ne 'udp' ) {
		error( $text{save_rule_error2} );
	}

	if( $src eq 'FIREWALL' && $dst eq 'FIREWALL' ) {
		error( $text{save_rule_error3} );
	}

	if( $src eq '' || $dst eq '' ) {
		error( $text{save_rule_error4} );
	}

	if( $target eq 'ACCEPT' && ($ndpi eq 'all' || $hostnameset ne '' || $riskset ne '') ) {
		error( $text{save_rule_error5} );
	}

	if( $target ne 'DROP' && $ratelimit ne '' ) {
		error( $text{save_rule_error6} );
	}

	if( $log ne '' && $ratelimit ne '' ) {
		error( $text{save_rule_error7} );
	}

	$fw->AddRule( $in{'new'} ? 0 : $idx, $src, $dst, $service, $ndpi, $category, $hostnameset, $riskset, $ratelimit, $port, $time, $target, $active, $log, $description );
}

$fw->SaveFirewall();
redirect( 'list_rules.cgi'.($in{'delete'} ? "?idx=$idx" : '') );
