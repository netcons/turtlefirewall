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

my $heading = '';
if( $new ) {
	$heading = "<img src=images/create.png hspace=4>$text{'edit_addresslist_title_create'}";
} else {
	$heading = "<img src=images/edit.png hspace=4>$text{'edit_addresslist_title_edit'}";
}
&ui_print_header( $heading, $text{'title'}, "" );

my $addresslist = $in{'addresslist'};
my $newaddresslist = $in{'newaddresslist'};
my %a = $fw->GetAddressList($addresslist);
my $location = $a{'LOCATION'};
my $type = $a{'TYPE'};
my $description = $a{'DESCRIPTION'};

my @types = ('hash:ip','hash:net','hash:mac');

print &ui_subheading($heading);
print &ui_form_start("save_addresslist.cgi", "post");
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("addresslist");
} else {
	$col = &ui_textbox("newaddresslist", $in{'addresslist'});
	$col .= &ui_hidden("addresslist", $in{'addresslist'});
}
print &ui_columns_row([ "<img src=images/db.png hspace=4><b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_textbox("location", $location, 60, 0, 60);
print &ui_columns_row([ "<img src=images/address.png hspace=4><b>$text{'location'}</b>", $col ], \@tds);
$col = &ui_select("type", $type, \@types);
print &ui_columns_row([ "<img src=images/option.png hspace=4><b>$text{'type'}</b>", $col ], \@tds);
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
