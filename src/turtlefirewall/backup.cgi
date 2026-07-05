#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
my $d = sprintf("%04d%02d%02d-%02d%02d", $year+1900, $mday+1, $mday, $hour, $min);
my $confdir = &confdir();

print "Content-Disposition: Attachment; filename=turtlefirewall-backup-$d.tar.gz\n";
print "X-Content-Type-Options: nosniff\n";
print "Content-type: application/x-gzip\n\n";
my $buffer = '';
open TARGZ, "tar cz --directory $confdir fw.xml fwuserdefservices.xml |"
	or &error( $text{configuration_error2} );
while(read( TARGZ, $buffer, &get_buffer_size_binary())) { print $buffer; }
close TARGZ;
