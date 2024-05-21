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
$hostnameset = $in{'hostnameset'};
$newhostnameset = $in{'newhostnameset'};

if( $new ) {
	&ui_print_header( "<img src=images/hostnameset.png hspace=4>$text{'edit_hostnameset_title_create'}", $text{'title'}, "" );
} else {
	&ui_print_header( "<img src=images/hostnameset.png hspace=4>$text{'edit_hostnameset_title_edit'}", $text{'title'}, "" );
}

my %h = $fw->GetHostNameSet($hostnameset);
my $hostnames = $h{'HOSTNAMES'};
my $description = $h{'DESCRIPTION'};

my @hostnamesetlist = split(/,/, $hostnames);

print &ui_subheading($new ? $text{'edit_hostnameset_title_create'} : $text{'edit_hostnameset_title_edit'});
print &ui_form_start("save_hostnameset.cgi", "post");
my @tds = ( "width=20% style=vertical-align:top", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
if( $new ) {
	$col = &ui_textbox("hostnameset");
} else {
	$col = &ui_textbox("newhostnameset", $in{'hostnameset'});
	$col .= &ui_hidden("hostnameset", $in{'hostnameset'});
}
print &ui_columns_row([ "<img src=images/hostnameset.png hspace=4><b>$text{'name'}</b>", $col ], \@tds);
$col = &ui_textarea("hostnamesetlist", join("\n", @hostnamesetlist), 10, 20);
print &ui_columns_row([ "<img src=images/hostname.png hspace=4><b>$text{'hostnames'}</b>", $col ], \@tds);
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
