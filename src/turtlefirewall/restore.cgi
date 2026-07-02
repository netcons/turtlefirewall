#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParseMime();

if( $in{backup} ) {
	my $backup = $in{backup};
	my $output = &tempname();
	my $confdir = &confdir();

	open TARGZ, "| tar xvz --directory $confdir fw.xml fwuserdefservices.xml >$output 2>&1" or &error( $text{backup_error1} );
	syswrite(TARGZ, $backup, length($backup));
	close TARGZ;

	&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_backup'}", $text{'title'}, "" );

	print qq~<table border="0" width="100%">
		<tr $tb>
			<th>$text{'backup_restoretitle'}</th>
		</tr>
		<tr $cb>
			<td style=text-align:center><pre>~;
	open FILE, "<$output";
	while( <FILE> ) { print; }
	close FILE;
	unlink $output;
	print qq~	</pre></td></tr></table>~;

	&ui_print_footer('index.cgi',$text{'index'});

} else {

	&error( $text{backup_error_title1} );

}
