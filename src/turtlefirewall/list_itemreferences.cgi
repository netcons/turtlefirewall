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

my $item = $in{'item'};

&ui_print_header( "$icons{SHIELD}{IMAGE}$text{'list_itemreferences_title'}", $text{'title'}, "" );

&showItemReferences();

&ui_print_footer('list_items.cgi','items list');

#============================================================================

sub showItemReferences {
	my $type = $fw->GetItemType($item);
	my $image = $icons{$type}{IMAGE};

	print &ui_subheading($image,$item);
	@tds = ();
        print &ui_columns_start([ "<b>$text{'references'}</b>" ], 100, 0, \@tds);
	my %itemreferences = $fw->GetItemReferences($item);
	foreach my $k (sort keys %itemreferences) {
		my $href = '';
		my $reftype = $itemreferences{$k};
		my $reftypelc = lc($reftype);
		my $prefix = $reftype eq 'RULE' ? 'filter' : $reftypelc;
		my @ks = split( / /, $k );
		my $refname = $ks[0];
		my $idx = $ks[1];
		# Item in Rule
		if( $idx ne '' ) {
			$idx++;
			my $refnamelc = lc($refname);
			$href = &ui_link("edit_$reftypelc.cgi?idx=$idx","$prefix rule id $idx $refnamelc");
		} else {
		# Item in Item
			$href = &ui_link("edit_$reftypelc.cgi?$reftypelc=$refname","$prefix item $refname");
		}
	        print &ui_columns_row([ "$icons{$reftype}{IMAGE}$href" ], \@tds);
        }
        print &ui_columns_end();
}
