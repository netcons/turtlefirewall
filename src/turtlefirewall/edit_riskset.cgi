#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';
&ReadParse();

$new = $in{'new'};
$riskset = $in{'riskset'};
$newriskset = $in{'newriskset'};

my $heading = '';
if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_riskset_title_create'}";
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_riskset_title_edit'}";
}
&ui_print_header( $heading, $text{'title'}, "" );

my %r = $fw->GetRiskSet($riskset);
my $risks = $r{'RISKS'};
my $description = $r{'DESCRIPTION'};

my $options_risk = '';
my @selected_risk = split(/,/, $risks);

&LoadNdpiRisks($fw);
my @items_risk = ();
my @risks = ();
push @risks, $fw->GetNdpiRisksList();
@risks = sort { $a <=> $b } @risks;
for my $k (@risks) {
	my $selected = 0;
	for my $s (@selected_risk) {
		if( $k eq $s ) {
			$selected = 1;
			last;
		}
	}
	my %risk = $fw->GetNdpiRisk($k);
	my @opts = ( "$k", "$k - $risk{DESCRIPTION}" );
	push(@items_risk, \@opts);
}

print &ui_subheading($heading);
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
print &ui_columns_row([ "$icons{RISKSET}{IMAGE}<b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_select("risks", \@selected_risk, \@items_risk, 5, 1);
print &ui_columns_row([ "$icons{RISK}{IMAGE}<b>$text{'risks'}</b>", $col ], \@tds);
$col = &ui_textbox("description", $description, 60, 0, 60);
print &ui_columns_row([ "$icons{DESCRIPTION}{IMAGE}<b>$text{'description'}</b>", $col ], \@tds);
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
