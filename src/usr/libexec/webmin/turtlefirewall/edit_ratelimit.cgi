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
$ratelimit = $in{'ratelimit'};
$newratelimit = $in{'newratelimit'};

if( $new ) {
	&ui_print_header( "<img src=images/ratelimit.png hspace=4>$text{'edit_ratelimit_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/ratelimit.png hspace=4>$text{'edit_ratelimit_title_edit'}", $text{'title'}, "" );
}

my %r = $fw->GetRateLimit($ratelimit);
my $rate = $r{'RATE'};
my $description = $r{'DESCRIPTION'};

print &ui_subheading($new ? $text{'edit_ratelimit_title_create'} : $text{'edit_ratelimit_title_edit'});
print &ui_form_start("save_ratelimit.cgi", "post");
my @tds = ( "width=20% style=vertical-align:top", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("ratelimit");
} else {
	$col = &ui_textbox("newratelimit", $in{'ratelimit'});
	$col .= &ui_hidden("ratelimit", $in{'ratelimit'});
}
print &ui_columns_row([ "<img src=images/ratelimit.png hspace=4><b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_textbox("rate", $rate, 3, 0, 3);
$col .= "<i>Mbps</i>";
print &ui_columns_row([ "<img src=images/rate.png hspace=4><b>$text{'rate'}</b>", $col ], \@tds);
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
