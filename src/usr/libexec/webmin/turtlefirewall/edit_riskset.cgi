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
	&ui_print_header( "<img src=images/riskset.png hspace=4>$text{'edit_riskset_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/riskset.png hspace=4>$text{'edit_riskset_title_edit'}", $text{'title'}, "" );
}

my %r = $fw->GetRiskSet($riskset);
my $risks = $r{'RISKS'};
my $description = $r{'DESCRIPTION'};

my $options_risk = '';
my @selected_risk = split(/,/, $risks);

&LoadNdpiRisks($fw);
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

print &ui_subheading($new ? $text{'edit_riskset_title_create'} : $text{'edit_riskset_title_edit'});
print &ui_form_start("save_riskset.cgi", "post");
my @tds = ( "width=20% style=vertical-align:top", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("riskset");
} else {
	$col = &ui_textbox("newriskset", $in{'riskset'});
	$col .= &ui_hidden("riskset", $in{'riskset'});
}
print &ui_columns_row([ "<img src=images/riskset.png hspace=4><b>$text{'name'}</b>", $col ], \@tds);
# FIXME
#$col = &ui_select("risks", \@selected_risk, \@items, 5, 1);
$col = "<select name=risks size=5 multiple>$options_risk</select>";
# FIXME
print &ui_columns_row([ "<img src=images/risk.png hspace=4><b>$text{'risks'}</b>", $col ], \@tds);
$col = &ui_textbox("description", $description, 60, 0, 60);
print &ui_columns_row([ "<img src=images/info.png hspace=4><b>$text{'description'}</b>", $col ], \@tds);
print &ui_columns_end();

print "<table width=100%><tr>";
if( $new ) {
        print '<td>'.&ui_submit( $text{'button_create'}, "new").'</td>';
} else {
        print '<td>'.&ui_submit( $text{'button_save'}, "save").'</td>';
        print '<td style=text-align:right>'.&ui_submit( $text{'button_delete'}, "delete").'</td>';
}
print "</tr></table>";

print &ui_form_end();

print "<br><br>";
&ui_print_footer('list_items.cgi','items list');
