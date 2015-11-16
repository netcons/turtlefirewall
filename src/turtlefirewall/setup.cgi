#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do '../web-lib.pl';
&init_config();
ReadParse();

&header( $text{'title'}, '', undef, 1 );

# do you need to install startup scripts?
if( -f "./setup/turtlefirewall" ) {

	my $err = 1;
	print "<br>";
	if( chdir("./setup") ) {
		$err = system( '/usr/bin/perl setup' );
		chdir("../");
	}
	if( $err == 0 ) {
		print "<br><br><b>Congratulation: Turtle Firewall successfully installed, ";
		print '<a href="index.cgi">Return to index.</a></b><br><br>';
		system( 'rm -rf setup' );
	} else {
		print "<b>Installation error, Turtle Firewall is not successfully installed!</b>";
	}
}

print "<br><br>\n";

&footer('/',$text{'index'});
