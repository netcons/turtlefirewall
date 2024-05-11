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

my $riskset = $in{'riskset'};
my $newriskset = $in{'newriskset'};
my $risks = $in{'risks'};
$risks =~ s/\0/,/g;
my $description = $in{'description'};

if( ! $fw->checkName($newriskset) ) { error( $text{save_riskset_error6} ); }

if( $in{'delete'} ) {
	# delete riskset
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $riskset = $d;
			$whatfailed = $text{save_riskset_error_title1};
			if( !$fw->DeleteRiskSet($riskset) ) { error( $text{save_riskset_error1} ); }
		}
	} elsif( $riskset ne '' ) {
		$whatfailed = $text{save_riskset_error_title1};
		if( !$fw->DeleteRiskSet($riskset) ) { error( $text{save_riskset_error1} ); }
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_riskset_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $riskset ) {
				error( $text{save_riskset_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_riskset_error_title3};
	}
	if ( $riskset eq '' ) { error( $text{save_riskset_error3} ); }
	if ( $riskset eq 'none' ) { error( $text{save_riskset_error7} ); }
	if ( $risks eq '' ) { error( $text{save_riskset_error4} ); }

	$fw->AddRiskSet( $riskset, $risks, $description );
	if( !$in{'new'} && $newriskset ne $riskset ) {
		if( !$fw->RenameItem( $riskset, $newriskset ) ) {
			error( text('save_riskset_error5', $riskset, $newriskset) );
		}
	}
}

$fw->SaveFirewall();
redirect( 'list_items.cgi' );
