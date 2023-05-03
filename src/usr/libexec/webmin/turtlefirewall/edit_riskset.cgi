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

$new = $in{'new'};
$riskset = $in{'riskset'};
$newriskset = $in{'newriskset'};

if( $new ) {
	&ui_print_header( $text{'edit_riskset_title_create'}, $text{'title'}, "" );
} else {
	&ui_print_header( $text{'edit_riskset_title_edit'}, $text{'title'}, "" );
}

my %r = $fw->GetRiskSet($riskset);
my $risks = $r{'RISKS'};
my $description = $r{'DESCRIPTION'};

my $options_risk = '';
my @selected_risk = split(/,/, $risks);

LoadNdpiRisks( $fw );
my @items = ();
push @items, $fw->GetNdpiRisksList();
@items = sort { $a <=> $b } @items;
for my $k (@items) {
	my $selected = 0;
	for my $s (@selected_risk) {
		if( $k eq $s ) {
			$selected = 1;
			last;
		}
	}
	my %risk = $fw->GetNdpiRisk($k);
	$options_risk .= qq~<option value="$k"~.($selected ? ' selected' : '').">$k - $risk{'DESCRIPTION'}</option>";
}

print "<br><br>
	<form action=\"save_riskset.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{'edit_riskset_title_create'} : $text{'edit_riskset_title_edit'})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\"><tr>
			<td>
				<b>".$text{'name'}."</b></td>
			<td>";
if( $new ) {
	print "		<input type=\"text\" name=\"riskset\">";
} else {
	print '		<input type="text" name="newriskset" value="'.$riskset.'">';
	print '		<input type="hidden" name="riskset" value="'.$riskset.'">';
}
print			qq~</td></tr>
                   	<tr>
                                <td><b>$text{'risks'}</b></td>
				<td><select name="risks" size="5" multiple>$options_risk</select></td>
			</tr>
 			<tr>
				<td><b>$text{'description'}</b></td>
				<td valign="top"><input type="text" name="description" size="60" value="$description"></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>~;

print "<table width=\"100%\"><tr>";
if( $new ) {
        print '<td>'.&ui_submit( $text{'button_create'}, "new").'</td>';
} else {
        print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
        print '<td align="right">'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&ui_print_footer('list_items.cgi','items list');
