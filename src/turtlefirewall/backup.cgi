#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();

if( $in{download} ) {
	&backup_download();
}

&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_backup'}", $text{'title'}, "" );

if( $in{upload} ) {
	# FIXME
	&restore_upload( $in{backup} );
	&ui_print_footer('backup.cgi',$text{'backup_title'});
	# FIXME
} else {
	print qq~<br/>
	<table border="0" width="100%">
	<tr $tb>
		<th>$text{'backup_backuptitle'}</th>
	</tr>
	<tr $cb>
		<td style=text-align:center>
		<br/>~;
	print   &ui_form_start("backup.cgi?download=1", "post");
	print   &ui_submit($text{'backup_index_download'});
	print   &ui_form_end();
	print qq~<br/><br/>
		</td>
	</tr>
	</table>

	<table border="0" width="100%">
	<tr $tb>
		<th>$text{'backup_restoretitle'}</th>
	</tr>
	<tr $cb>
		<td style=text-align:center>
		<br/>~;
	print   &ui_form_start("backup.cgi", "form-data");
	print 	&ui_upload("backup", 40);
	print 	&ui_submit($text{'backup_index_restore'});
	print   &ui_form_end();
	print qq~<br/><br/>
		<br/>
		</td>
	</tr>
	</table><br>~;

	&ui_print_footer('index.cgi',$text{'index'});
}

sub backup_download {
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	my $d = sprintf("%04d%02d%02d-%02d%02d", $year+1900, $mday+1, $mday, $hour, $min);
	my $confdir = &confdir();

	open TARGZ, "tar cz --directory $confdir fw.xml fwuserdefservices.xml |"
		or &error( "Error during backup" );
	print "Content-type: application/x-gzip\n";
	print "Expires: Mon, 26 Jul 1997 05:00:00 GMT\n";    # Date in the past
	print "Cache-Control: no-store, no-cache, must-revalidate\n";  # HTTP/1.1
	print "Cache-Control: post-check=0, pre-check=0\n";
	#print "Pragma: no-cache\n";
	print "Content-Disposition: inline; filename=turtlefirewall-backup-$d.tar.gz\n";
	print "\n";
	my $buffer = '';
	while( read( TARGZ, $buffer, 1024) ) {
		print $buffer;
	}
	close TARGZ;
	exit 0;
}

sub restore_upload {
	my $backup = shift;
	my $output = &tempname();
	my $confdir = &confdir();

	$whatfailed = $text{backup_error_title1};

	#chdir '/etc/turtlefirewall';
	#chdir '/tmp';
	open TARGZ, "| tar xvz --directory $confdir fw.xml fwuserdefservices.xml >$output 2>&1" or &error( $text{backup_error1} );
	syswrite(TARGZ, $backup, length($backup));
	close TARGZ;

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
}
