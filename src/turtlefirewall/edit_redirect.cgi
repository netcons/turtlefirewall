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

my $nRedirect = $fw->GetRedirectCount();

$new = $in{'new'};

if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_redirect_title_create'}";
	$nRedirect++;
	$idx = $nRedirect;
	$newIdx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$toport = '';
	$is_redirect = 1;
	$active = 1;
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_redirect_title_edit'}";
	$idx = $in{'idx'};
	$newIdx = '';
	%redirect = $fw->GetRedirect($idx);
	$src = $redirect{'SRC'};
	$dst = $redirect{'DST'};
	$service = $redirect{'SERVICE'};
	$port = $redirect{'PORT'};
	$toport = $redirect{'TOPORT'};
	$is_redirect = $redirect{'REDIRECT'} ne 'NO';
	$active = $redirect{'ACTIVE'} ne 'NO';
}
&ui_print_header( $heading, $text{'title'}, "" );

my @idxs = ();
for( my $i=1; $i<=$nRedirect; $i++ ) { push @idxs, $i; }

my @items_src = ();
push @items_src, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_src, $fw->GetNetList();
push @items_src, $fw->GetHostList();
push @items_src, $fw->GetGroupList();
push @items_src, $fw->GetGeoipList();
push @items_src, $fw->GetIPSetList();
@items_src = sort(@items_src);

my @items_dst = ('*');
# I cannot specify a zone as destination (iptables PREROUTING cant have -o option)
#push @items_dst, grep(!/FIREWALL/, $fw->GetZoneList());
push @items_dst, $fw->GetNetList();
push @items_dst, $fw->GetHostList();
push @items_dst, $fw->GetGroupList();
push @items_dst, $fw->GetGeoipList();
push @items_dst, $fw->GetIPSetList();
@items_dst = sort(@items_dst);

print &ui_subheading($heading);
print &ui_form_start("save_redirect.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
$col = &ui_select("newIdx", $idx, \@idxs);
print &ui_columns_row([ "$icons{ID}{IMAGE}<b>ID</b>", $col ], \@tds);
$col = &ui_select("src", $src, \@items_src);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'redirect_src'}</b>", $col ], \@tds);
$col = &ui_select("dst", $dst, \@items_dst);
$col .= "<small><i>$text{preroute_help}</i></small>";
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'redirect_dst'}</b>", $col ], \@tds);
$col = &formService($service, $port, 1);
print &ui_columns_row([ "$icons{SERVICE}{IMAGE}<b>$text{'rule_service'}</b>", $col ], \@tds);
my @opts = ( [ 0, "$text{NO}<br>" ], [ 1, "$text{YES}" ] );
$col = &ui_radio("redirect", $is_redirect ? 1 : 0, \@opts);
$col .= " : $text{redirect_toport} : ";
$col .= &ui_textbox("toport", $toport, 5, 0, 5);
print &ui_columns_row([ "$icons{REDIRECT}{IMAGE}<b>$text{'redirect_redirect'}</b>", $col ], \@tds);
$col = &ui_checkbox("active", 1, undef, $active ? 1 : 0);
print &ui_columns_row([ "$icons{ACTIVE}{IMAGE}<b>$text{'redirect_active'}</b>", $col ], \@tds);
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
&ui_print_footer("list_nat.cgi?table=redirect&idx=$idx",'NAT list');
