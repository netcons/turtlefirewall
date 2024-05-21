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

my $hostnameset = $in{'hostnameset'};
my $newhostnameset = $in{'newhostnameset'};
my $hostnamesetlist = $in{'hostnamesetlist'};
my $description = $in{'description'};

$hostnamesetlist =~ s/^\s+|\s+$//g;

if( ! $fw->checkName($newhostnameset) ) { &error( $text{save_hostnameset_error6} ); }

if( $in{'delete'} ) {
	# delete hostnameset
	if( $in{'d'} ) {
		@d = split(/\0/, $in{'d'});
		foreach $d (sort { $b <=> $a } @d) {
			my $hostnameset = $d;
			$whatfailed = $text{save_hostnameset_error_title1};
			if( !$fw->DeleteHostNameSet($hostnameset) ) { &error( $text{save_hostnameset_error1} ); }
		}
	} elsif( $hostnameset ne '' ) {
		$whatfailed = $text{save_hostnameset_error_title1};
		if( !$fw->DeleteHostNameSet($hostnameset) ) { &error( $text{save_hostnameset_error1} ); }
	}
} else {
	if( $in{'new'} ) {
		$whatfailed = $text{save_hostnameset_error_title2};
		my @allitems = $fw->GetAllItemsList();
		foreach my $i (@allitems) {
			if( $i eq $hostnameset ) {
				&error( $text{save_hostnameset_error2} );
			}
		}
	} else {
		$whatfailed = $text{save_hostnameset_error_title3};
	}
	if ( $hostnameset eq '' ) { &error( $text{save_hostnameset_error3} ); }
	if ( $hostnameset eq 'any' ) { &error( $text{save_hostnameset_error8} ); }
	if ( $hostnamesetlist eq '' ) { 
		&error( $text{save_hostnameset_error4} );
	} else {
		for my $hostname (split(/\s+/, $hostnamesetlist)) {
			if ( $hostname ne '' && $hostname !~ /^[A-z0-9\-\.]+$/ ) { 
				&error( $text{save_hostnameset_error7} );
	       		}
		}
	}
	$hostnames = $hostnamesetlist;
	$hostnames =~ s/\s+/,/g;
	$fw->AddHostNameSet( $hostnameset, $hostnames, $description );
	if( !$in{'new'} && $newhostnameset ne $hostnameset ) {
		if( !$fw->RenameItem( $hostnameset, $newhostnameset ) ) {
			&error( $text('save_hostnameset_error5', $hostnameset, $newhostnameset) );
		}
	}
}

$fw->SaveFirewall();
&redirect( 'list_items.cgi' );
