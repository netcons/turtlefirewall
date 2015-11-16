#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================


do 'lib.pl';

$new = $in{'new'};

if( $new ) {
	&header( $text{edit_rule_title_create}, '' );
	$idx = '';
	$src = '';
	$dst = '';
	$service = '';
	$port = '';
	$target = '';
	$mark = '';
	$active = 1;
	$description = '';
} else {
	&header( $text{edit_rule_title_edit}, '' );
	$idx = $in{'idx'};
	%rule = $fw->GetRule($idx);
	$src = $rule{'SRC'};
	$dst = $rule{'DST'};
	$service = $rule{'SERVICE'};
	$port = $rule{'PORT'};
	$target = $rule{'TARGET'};
	$mark = $rule{'MARK'};
	$active = $rule{'ACTIVE'} ne 'NO';
	$description = $rule{'DESCRIPTION'};
}

my $options_src = '';
my $options_dst = '';
my @selected_src = split(/,/, $src);
my @selected_dst = split(/,/, $dst);
my @items = ('*');
push @items, $fw->GetZoneList();
push @items, $fw->GetNetList();
push @items, $fw->GetHostList();
push @items, $fw->GetGroupList();
@items = sort(@items);
for my $k (@items) {
	my $selected = 0;
	for my $s (@selected_src) {
		if( $k eq $s ) {
			$selected = 1;
			last;
		}
	}
	$options_src .= '<option'.($selected ? ' selected' : '').'>'.$k;
	$selected = 0;
	for my $s (@selected_dst) {
		if( $k eq $s ) {
			$selected = 1;
			last;
		}
	}
	$options_dst .= '<option'.($selected ? ' selected' : '').'>'.$k;
}

print "<br>
	<form action=\"save_rule.cgi\">
	<input type=\"hidden\" name=\"idx\" value=\"$idx\">
	<table border width=\"100%\">
		<tr $tb>
			<th>".($new ? $text{edit_rule_title_create} : $text{edit_rule_title_edit})."</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\">";
if( !$new ) {
	print		"<tr>
				<td><b>#</b></td>
				<td><b><tt>$idx</tt></b></td>
			</tr>";
}
print			"<tr>
				<td><b>$text{rule_src}</b></td>
				<td><select name=\"src\" size=\"5\" multiple>$options_src</select></td>
			</tr>
			<tr>
				<td><b>$text{rule_dst}</b></td>
				<td><select name=\"dst\" size=\"5\" multiple>$options_dst</select></td>
			</tr>
			<tr>
				<td><b>$text{rule_service}</b></td>
				<td><br>";
				formService( $service, $port, 1 );
print				"<br>
				</td>
			</tr>
			<tr>
				<td><b>$text{rule_target}</b></td>
				<td>
				<select name=\"target\">
				<option ".($target eq 'ACCEPT' ? 'SELECTED' : '').">ACCEPT</option>
				<option ".($target eq 'DROP' ? 'SELECTED' : '').">DROP</option>
				<option ".($target eq 'REJECT' ? 'SELECTED' : '').">REJECT</option>
				</select>
				</td>
			</tr>
			<tr>
				<td><b>$text{rule_mark}</b></td>
				<td><input type=\"text\" name=\"mark\" value=\"$mark\" size=\"13\"></td>
			</tr>
			<tr>
				<td><b>$text{rule_active}</b></td>
				<td><input type=\"checkbox\" name=\"active\" value=\"1\"".($active ? ' checked' : '')."></td>
			</tr>
			<tr>
				<td><b>$text{description}</b></td>
				<td><input type=\"text\" name=\"description\" value=\"$description\" size=\"60\"></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>";

print "<table width=\"100%\"><tr>";
if( $new ) {
	print '<td><input type="submit" name="new" value="'.$text{button_create}.'"></td>';
} else {
	print '<td><input type="submit" name="save" value="'.$text{button_save}.'"></td>';
	print '<td align="right"><input type="submit" name="delete" value="'.$text{button_delete}.'"></td>';
}
print "</tr></table>";
print "</form>";

print "<br><br>";
&footer("list_rules.cgi?idx=$idx",'Rules list');


