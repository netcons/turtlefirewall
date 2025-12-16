#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) 2001-2026 Andrea Frigido <andrea@frisoft.it>
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

require './turtlefirewall-lib.pl';
&ReadParse();

$nNat = $fw->GetNatsCount();

$new = $in{'new'};

if( $new ) {
	$heading = "$icons{CREATE}{IMAGE}$text{'edit_nat_title_create'}";
	$nNat++;
	$idx = $nNat;
	$newIdx = '';
	$virtual = '';
	$real = '';
	$service = '';
	$port = '';
        $toport = '';
	$active = 1;
} else {
	$heading = "$icons{EDIT}{IMAGE}$text{'edit_nat_title_edit'}";
	$idx = $in{'idx'};
	$newIdx = '';
	%nat = $fw->GetNat($idx);
	$virtual = $nat{'VIRTUAL'};
	$real = $nat{'REAL'};
	$service = $nat{'SERVICE'};
	$port = $nat{'PORT'};
        $toport = $nat{'TOPORT'};
	$active = $nat{'ACTIVE'} ne 'NO';
}
&ui_print_header( "$icons{ICON}{IMAGE}$text{'index_icon_nat'}", $text{'title'}, "" );

my @idxs = ();
for( my $i=1; $i<=$nNat; $i++ ) { push @idxs, $i; }

my @items_virtual = ();
my @virtuals = ();
push @virtuals, grep(!/FIREWALL/, $fw->GetZoneList());
push @virtuals, $fw->GetHostList();
for my $k (sort @virtuals) {
	my @opts = ();
	my %zone = $fw->GetZone($k);
	if( $zone{IF} ne '' ) {
		@opts = ( "$k", "$k ($zone{IF})" );
	} else {
		@opts = ( "$k", "$k" );
	}
	push(@items_virtual, \@opts);
}

my @items_real = ();
push @items_real, $fw->GetHostList();

print &ui_subheading($heading);
print &ui_form_start("save_nat.cgi", "post");
print &ui_hidden("idx", $idx);
my @tds = ( "width=20%", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
$col = &ui_select("newIdx", $idx, \@idxs);
print &ui_columns_row([ "$icons{ID}{IMAGE}<b>ID</b>", $col ], \@tds);
$col = &ui_select("virtual", $virtual, \@items_virtual);
print &ui_columns_row([ "$icons{ZONE}{IMAGE}<b>$text{'virtual_host'}</b>", $col ], \@tds);
$col = &ui_select("real", $real, \@items_real);
print &ui_columns_row([ "$icons{HOST}{IMAGE}<b>$text{'real_host'}</b>", $col ], \@tds);
$col = &formService($service, $port, 1);
print &ui_columns_row([ "$icons{SERVICE}{IMAGE}<b>$text{'rule_service'}</b>", $col ], \@tds);
my @opts = ( [ 1, "$text{YES}" ] );
$col = &ui_radio("dummy", 1, \@opts);
$col .= " : $text{real_port} $text{nat_port} : ";
$col .= &ui_textbox("toport", $toport, 5, 0, 5);
print &ui_columns_row([ "$icons{NAT}{IMAGE}<b>$text{'nat'}</b>", $col ], \@tds);
$col = &ui_checkbox("active", 1, undef, $active ? 1 : 0);
print &ui_columns_row([ "$icons{ACTIVE}{IMAGE}<b>$text{'nat_active'}</b>", $col ], \@tds);
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
&ui_print_footer("list_nat.cgi?table=nat&idx=$idx",'NAT list');
