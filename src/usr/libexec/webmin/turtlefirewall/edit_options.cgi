#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( "<img src=images/shield.png hspace=4>$text{'edit_options_title'}", $text{'title'}, "" );

getOptionsList();

foreach $option (@optionkeys) {
	$options{$option}{value} = $fw->GetOption( $option );
	if( $options{$option}{value} eq '' ) {
		$options{$option}{value} = $options{$option}{default};
	}
}

print qq~<br>
	<form action="save_options.cgi">
	<table border width="100%">
		<tr $tb>
			<th>$text{edit_options_title}</th>
		</tr>
		<tr $cb>
			<td>
			<table width="100%" border>~;

foreach $option (@optionkeys) {
	showOption( $option, $options{$option}{type}, $options{$option}{value},
		$options{$option}{default}, $options{$option}{addunchangeopz},
		$text{"options_${option}_name"}, $text{"options_${option}_desc"} );
}

print qq~			</table>
			</td>
		</tr>
	</table>

	<table width="100%"><tr>~;
print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
print qq~	</tr></table>
	</form>
	<br><br>~;

&ui_print_footer('','turtle firewall index');

sub showOption {
	my( $var, $type, $value, $default, $addunchangeopz, $name, $desc ) = @_;
	print qq|
			<tr>
				<td valign="top">
					<b>$name</b>
				</td>
				<td valign="top"><nobr>|;
	if( $type eq 'radio' ) {
		print qq|		<input type="radio" name="$var" value="on"|.($value eq 'on' ? ' checked':'').qq|> on
					<input type="radio" name="$var" value="off"|.($value eq 'off' ? ' checked':'').'> off';
	}
	if( $type eq 'text' ) {
		print qq|		<input type="text" name="$var" value="$value">|;
	}
	if( $addunchangeopz ) {
		print qq|		<input type="radio" name="$var" value="unchange"|.($value eq 'unchange' ? ' checked':'').'> unchange';
	}
	print qq|
				</nobr></td>
				<td valign="top">
					$desc<br>
					Default: <b>$default</b>
				</td>
			</tr>|;
}
