#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

if( $in{download} ) {
	backup_download();
}

&ui_print_header( $text{'backup_title'}, $text{'title'}, "" );

if( $in{upload} ) {
	restore_upload( $in{backup} );
	&ui_print_footer('backup.cgi',$text{'backup_title'});
} else {
	print qq~<br/>
	<table border width="100%">
	<tr $tb>
		<th>$text{'backup_backuptitle'}</th>
	</tr>
	<tr $cb>
		<td align="center">
		<br/>~;
	#	<a href="backup.cgi?download=1"><b>$text{backup_backupdownload}</b></a>
		print &ui_buttons_row("backup.cgi?download=1", $text{backup_backupdownload});
	print qq~<br/><br/>
		</td>
	</tr>
	</table>

	<table border width="100%">
	<tr $tb>
		<th>$text{'backup_restoretitle'}</th>
	</tr>
	<tr $cb>
		<td align="center">
		<br/>
		<form action="backup.cgi" method="POST" enctype="multipart/form-data">~;
	#	<input name="backup" type="file" size="40">&nbsp~;
	print 	&ui_upload("backup", 40);
	#	<input name="upload" type="submit" value="$text{backup_restoreupload}">
	print 	&ui_submit($text{'backup_restoreupload'}, "upload");
	print qq~</form>
		<br/>
		</td>
	</tr>
	</table><br>~;

	&ui_print_footer('','turtle firewall index');
}

sub backup_download {
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	my $d = sprintf("%04d%02d%02d-%02d%02d", $year+1900, $mday+1, $mday, $hour, $min);
	my $confdir = confdir();

	open TARGZ, "tar cz --directory $confdir fw.xml fwuserdefservices.xml |"
		or error( "Errore in fase di backup" );
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
	my $output = tempname();
	my $confdir = confdir();

	$whatfailed = $text{backup_error_title1};

	#chdir '/etc/turtlefirewall';
	#chdir '/tmp';
	open TARGZ, "| tar xvz --directory $confdir fw.xml fwuserdefservices.xml >$output 2>&1" or error( $text{backup_error1} );
	syswrite(TARGZ, $backup, length($backup));
	close TARGZ;

	print qq~<table border width="100%">
		<tr $tb>
			<th>$text{'backup_restoretitle'}</th>
		</tr>
		<tr $cb>
			<td align="center"><pre><tt>~;
	open FILE, "<$output";
	while( <FILE> ) { print; }
	close FILE;
	unlink $output;
	print qq~	</tt></pre></td></tr></table>~;
}
