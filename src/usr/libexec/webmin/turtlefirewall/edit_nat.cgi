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

if( $new ) {
	&ui_print_header( "<img src=images/grey-nat.png hspace=4>$text{'edit_nat_title_create'}", $text{'title'}, "" );
	$idx = '';
	$virtual = '';
	$real = '';
	$service = '';
	$port = '';
        $toport = '';
	$active = 1;
} else {
	&ui_print_header( "<img src=images/grey-nat.png hspace=4>$text{'edit_nat_title_edit'}", $text{'title'}, "" );
	$idx = $in{'idx'};
	%nat = $fw->GetNat($idx);
	$virtual = $nat{'VIRTUAL'};
	$real = $nat{'REAL'};
	$service = $nat{'SERVICE'};
	$port = $nat{'PORT'};
        $toport = $nat{'TOPORT'};
	$active = $nat{'ACTIVE'} ne 'NO';
}


my @items_virtual = ();
push @items_virtual, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_virtual, $fw->GetHostList();

my @items_real = ();
push @items_real, $fw->GetHostList();

print &ui_subheading($new ? $text{'edit_nat_title_create'} : $text{'edit_nat_title_edit'});
print &ui_form_start("save_nat.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( !$new ) {
	$col = "<b>$idx</b>";
	print &ui_columns_row([ "<img src=images/hash.png hspace=4><b>ID</b>", $col ], \@tds);
}
$col = &ui_select("virtual", $virtual, \@items_virtual);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'virtual_host'}</b>", $col ], \@tds);
$col = &ui_select("real", $real, \@items_real);
print &ui_columns_row([ "<img src=images/host.png hspace=4><b>$text{'real_host'}</b>", $col ], \@tds);
$col = &formService($service, $port, 1);
print &ui_columns_row([ "<img src=images/service.png hspace=4><b>$text{'rule_service'}</b>", $col ], \@tds);
my @opts = ( [ 1, "$text{YES}" ] );
$col = &ui_radio("dummy", 1, \@opts);
$col .= " : $text{real_port} $text{nat_port} : ";
$col .= &ui_textbox("toport", $toport, 5, 0, 5);
print &ui_columns_row([ "<img src=images/grey-nat.png hspace=4><b>$text{'nat'}</b>", $col ], \@tds);
$col = &ui_checkbox("active", 1, undef, $active ? 1 : 0);
print &ui_columns_row([ "<img src=images/active.png hspace=4><b>$text{'nat_active'}</b>", $col ], \@tds);
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
&ui_print_footer('list_nat.cgi','NAT list');
