#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2025 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();

my $nMasq = $fw->GetMasqueradesCount();

$new = $in{'new'};

if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_masq_title_create'}";
	$nMasq++;
	$idx = $nMasq;
	$newIdx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$is_masquerade = 1;
	$active = 1;
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_masq_title_edit'}";
	$idx = $in{'idx'};
	$newIdx = '';
	%masq = $fw->GetMasquerade($idx);
	$src = $masq{'SRC'};
	$dst = $masq{'DST'};
	$service = $masq{'SERVICE'};
	$port = $masq{'PORT'};
	$is_masquerade = $masq{'MASQUERADE'} ne 'NO';
	$active = $masq{'ACTIVE'} ne 'NO';
}
&ui_print_header( $heading, $text{'title'}, "" );

my @idxs = ();
for( my $i=1; $i<=$nMasq; $i++ ) { push @idxs, $i; }

my @items_src = ('*');
push @items_src, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_src, $fw->GetNetList();
push @items_src, $fw->GetHostList();
push @items_src, $fw->GetGroupList();
push @items_src, $fw->GetGeoipList();
push @items_src, $fw->GetIPSetList();
@items_src = sort(@items_src);

my @items_dst = ();
push @items_dst, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_dst, $fw->GetNetList();
push @items_dst, $fw->GetHostList();
push @items_dst, $fw->GetGroupList();
push @items_dst, $fw->GetGeoipList();
push @items_dst, $fw->GetIPSetList();
@items_dst = sort(@items_dst);

print &ui_subheading($heading);
print &ui_form_start("save_masquerade.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
$col = &ui_select("newIdx", $idx, \@idxs);
print &ui_columns_row([ "$icons{ID}{IMAGE}<b>ID</b>", $col ], \@tds);
$col = &ui_select("src", $src, \@items_src);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'masq_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", $dst, \@items_dst);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'masq_dst'}</b>", $col ], \@tds);
$col = &formService($service, $port, 1);
print &ui_columns_row([ "$icons{SERVICE}{IMAGE}<b>$text{'rule_service'}</b>", $col ], \@tds);
my @opts = ( [ 0, "$text{NO}<br>" ], [ 1, $text{YES} ] );
$col = &ui_radio("masquerade", $is_masquerade ? 1 : 0, \@opts);
print &ui_columns_row([ "$icons{MASQUERADE}{IMAGE}<b>$text{'masq_masquerade'}</b>", $col ], \@tds);
$col = &ui_checkbox("active", 1, undef, $active ? 1 : 0);
print &ui_columns_row([ "$icons{ACTIVE}{IMAGE}<b>$text{'masq_active'}</b>", $col ], \@tds);
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
&ui_print_footer("list_nat.cgi?table=masquerade&idx=$idx",'NAT list');
