#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( "<img src=images/edit.png hspace=4>$text{'edit_options_title'}", $text{'title'}, "" );

&getOptionsList();

foreach $option (@optionkeys) {
	$options{$option}{value} = $fw->GetOption( $option );
	if( $options{$option}{value} eq '' ) {
		$options{$option}{value} = $options{$option}{default};
	}
}

print &ui_subheading("<img src=images/edit.png hspace=4>$text{'edit_options_title'}");
print &ui_form_start("save_options.cgi", "post");
my @tds = ( "width=20% style=vertical-align:top", "width=20%", "width=60%" );
print &ui_columns_start(undef, 100, 0, \@tds);
foreach $option (@optionkeys) {
	&showOption( $option, $options{$option}{type}, $options{$option}{value},
		$options{$option}{default}, $options{$option}{addunchangeopz},
		$text{"options_${option}_name"}, $text{"options_${option}_desc"} );
}
print &ui_columns_end();

print "<table width=100%><tr>";
print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
print "</tr></table>";

print &ui_form_end();

print "<br><br>";
&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showOption {
	my( $var, $type, $value, $default, $addunchangeopz, $name, $desc ) = @_;
	my $col = '';
	if( $type eq 'radio' ) {
		my @opts = ();
		if( $addunchangeopz ) {
			@opts = ( [ "off", $text{off} ], [ "on", $text{on} ], [ "unchange", $text{unchange} ] );
		} else {
			@opts = ( [ "off", $text{off} ], [ "on", $text{on} ] );
		}
		$col = &ui_radio($var, $value, \@opts);
	}
	if( $type eq 'text' ) {
		$col = &ui_textbox($var, $value);
	}
	print &ui_columns_row([ "<img src=images/option.png hspace=4><b>$name</b>", $col, "$desc<br>Default: <b>$default</b>" ], \@tds);
}
