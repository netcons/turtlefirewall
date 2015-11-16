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
$src =~ s/\0/,/g;
my $dst = $in{'dst'};
$dst =~ s/\0/,/g;
my ($service, $port) = formServiceParse( $in{'servicetype'}, $in{'service2'}, $in{'service3'}, $in{'port'} );
my $target = $in{'target'};
my $mark = $in{'mark'};
my $active = $in{'active'};
my $description = $in{'description'};

if( $in{'delete'} ) {
	# delete rule
	$whatfailed = $text{save_rule_error_title1};
	$fw->DeleteRule( $idx );
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

	if( $mark ne '' && $mark !~ /^(0x[A-Fa-f0-9]+|[0-9]+)$/ ) {
		error( $text{save_rule_error4} );
	}
		
	$fw->AddRule( $in{'new'} ? 0 : $idx, $src, $dst, $service, $port, $target, $mark, $active, $description );
}

$fw->SaveFirewall();
redirect( 'list_rules.cgi'.($in{'delete'} ? "?idx=$idx" : '') );
