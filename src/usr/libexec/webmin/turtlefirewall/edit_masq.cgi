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
	&ui_print_header( "<img src=images/grey-nat.png hspace=4>$text{'edit_masq_title_create'}", $text{'title'}, "" );
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$is_masquerade = 1;
	$active = 1;
} else {
	&ui_print_header( "<img src=images/grey-nat.png hspace=4>$text{'edit_masq_title_edit'}", $text{'title'}, "" );
	$idx = $in{'idx'};
	%masq = $fw->GetMasquerade($idx);
	$src = $masq{'SRC'};
	$dst = $masq{'DST'};
	$service = $masq{'SERVICE'};
	$port = $masq{'PORT'};
	$is_masquerade = $masq{'MASQUERADE'} ne 'NO';
	$active = $masq{'ACTIVE'} ne 'NO';
}

my @items_src = ('*');
push @items_src, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_src, $fw->GetNetList();
push @items_src, $fw->GetHostList();
push @items_src, $fw->GetGroupList();
@items_src = sort(@items_src);

my @items_dst = ();
push @items_dst, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_dst, $fw->GetNetList();
push @items_dst, $fw->GetHostList();
push @items_dst, $fw->GetGroupList();
@items_dst = sort(@items_dst);

print &ui_subheading($new ? $text{'edit_masq_title_create'} : $text{'edit_masq_title_edit'});
print &ui_form_start("save_masq.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( !$new ) {
	$col = "<b>$idx</b>";
	print &ui_columns_row([ "<img src=images/hash.png hspace=4><b>ID</b>", $col ], \@tds);
}
$col = &ui_select("src", $src, \@items_src);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'masq_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", $dst, \@items_dst);
print &ui_columns_row([ "<img src=images/zone.png hspace=4><b>$text{'masq_dst'}</b>", $col ], \@tds);
$col = &formService($service, $port, 1);
print &ui_columns_row([ "<img src=images/service.png hspace=4><b>$text{'rule_service'}</b>", $col ], \@tds);
my @opts = ( [ 0, "$text{NO}<br>" ], [ 1, $text{YES} ] );
$col = &ui_radio("masquerade", $is_masquerade ? 1 : 0, \@opts);
print &ui_columns_row([ "<img src=images/grey-nat.png hspace=4><b>$text{'masq_masquerade'}</b>", $col ], \@tds);
$col = &ui_checkbox("active", 1, undef, $active ? 1 : 0);
print &ui_columns_row([ "<img src=images/active.png hspace=4><b>$text{'masq_active'}</b>", $col ], \@tds);
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
