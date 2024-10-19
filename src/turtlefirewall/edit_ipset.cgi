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
use File::Basename;

$new = $in{'new'};

my $heading = '';
if( $new ) {
	$heading = "<img src=images/create.png hspace=4>$text{'edit_ipset_title_create'}";
} else {
	$heading = "<img src=images/edit.png hspace=4>$text{'edit_ipset_title_edit'}";
}
&ui_print_header( $heading, $text{'title'}, "" );

my $ipset = $in{'ipset'};
my $newipset = $in{'newipset'};
my %n = $fw->GetIPSet($ipset);
my $ip = $n{'IP'};
my $zone = $n{'ZONE'};
my $description = $n{'DESCRIPTION'};

my $confdir = &confdir();

my @items_ipsetlist = ();
my @ipsetlists = glob("$confdir/*.ipset");
for my $k (@ipsetlists) {
	my $ip = basename($k, ".ipset");
	my @opts = ( "$ip", "$ip - $k" );
	push(@items_ipsetlist, \@opts);
}

my @zones = grep(!/FIREWALL/, $fw->GetZoneList());

print &ui_subheading($heading);
print &ui_form_start("save_ipset.cgi", "post");
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("ipset");
} else {
	$col = &ui_textbox("newipset", $in{'ipset'});
	$col .= &ui_hidden("ipset", $in{'ipset'});
}
print &ui_columns_row([ "<img src=images/item.png hspace=4><b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_select("ip", $ip, \@items_ipsetlist);
$col .= "<small><i>$text{ipset_help}</i></small>";
print &ui_columns_row([ "<img src=images/address.png hspace=4><b>$text{'location'}</b>", $col ], \@tds);
$col = &ui_select("zone", $zone, \@zones);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'zone'}</b>", $col ], \@tds);
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
