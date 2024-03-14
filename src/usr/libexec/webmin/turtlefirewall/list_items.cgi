#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( "<img src=images/shield.png hspace=4>$text{'list_items_title'}", $text{'title'}, "" );

$form = 0;
showZone();

$form++;
print "<br><br>";
showNet();

$form++;
print "<br><br>";
showHost();

$form++;
print "<br><br>";
LoadCountryCodes( $fw );
showGeoip();

$form++;
print "<br><br>";
showGroup();

$form++;
print "<br><br>";
showTime();

$form++;
print "<br><br>";
showTimeGroup();

$form++;
print "<br><br>";
showHostNameSet();

$form++;
print "<br><br>";
LoadNdpiRisks( $fw );
showRiskSet();

$form++;
print "<br><br>";
showRateLimit();

&ui_print_footer('','turtle firewall index');

#============================================================================

sub showZone {
	print &ui_form_start("save_zone.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_zone.cgi?new=1\">$text{'list_items_create_zone'}</a>" );
        @tds = ( "width=1% valign=top",
		 "",
		 "",
		 "" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'interface'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetZoneList()) {
		my %zone = $fw->GetZone($k);
		local @cols;
		my $href = &ui_link("edit_zone.cgi?zone=$k",$k);
		if( $k eq 'FIREWALL' ) {
			push(@cols, "<img src=images/firewall.png hspace=4><i>$k</i>" );
		} else {
			push(@cols, "<img src=images/zone.png hspace=4>$href" );
		}
		push(@cols, "$zone{'IF'}" );
		push(@cols, "".($zone{'DESCRIPTION'} ne '' ? $zone{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showNet {
	print &ui_form_start("save_net.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_net.cgi?new=1\">$text{'list_items_create_net'}</a>" );
        @tds = ( "width=1% valign=top",
		 "",
		 "",
		 "",
		 "",
		 "" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'net'}</b>",
                          "<b>$text{'netaddress'}</b>",
                          "<b>$text{'netmask'}</b>",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetNetList()) {
		my %net = $fw->GetNet($k);
		local @cols;
		my $href = &ui_link("edit_net.cgi?net=$k",$k);
		push(@cols, "<img src=images/net.png hspace=4>$href" );
	        push(@cols, "$net{'IP'}" );
	        push(@cols, "$net{'NETMASK'}" );
	        push(@cols, "$net{'ZONE'}" );
	        push(@cols, "".($net{'DESCRIPTION'} ne '' ? $net{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showHost {
	print &ui_form_start("save_host.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_host.cgi?new=1\">$text{'list_items_create_host'}</a>" );
        @tds = ( "width=1% valign=top",
		 "",
		 "",
		 "",
		 "",
		 "" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'host'}</b>",
                          "<b>$text{'hostaddress'}</b>",
                          "<b>$text{'macaddress'}</b>",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetHostList()) {
		my %host = $fw->GetHost($k);
		local @cols;
		my $href = &ui_link("edit_host.cgi?host=$k",$k);
		push(@cols, "<img src=images/host.png hspace=4>$href" );
	        push(@cols, "$host{'IP'}" );
	        push(@cols, "$host{'MAC'}" );
	        push(@cols, "$host{'ZONE'}" );
	        push(@cols, "".($host{'DESCRIPTION'} ne '' ? $host{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showGeoip {
	print &ui_form_start("save_geoip.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_geoip.cgi?new=1\">$text{'list_items_create_geoip'}</a>" );
        @tds = ( "width=1% valign=top",
		 "",
		 "",
		 "",
		 "" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'geoip'}</b>",
                          "<b>$text{'countrycode'}</b>",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetGeoipList()) {
		my %geoip = $fw->GetGeoip($k);
		local @cols;
		my $href = &ui_link("edit_geoip.cgi?geoip=$k",$k);
		push(@cols, "<img src=images/geoip.png hspace=4>$href" );
		my %g = $fw->GetCountryCode($geoip{'IP'});
		push(@cols, "$geoip{'IP'} - $g{'DESCRIPTION'}" );
	        push(@cols, "$geoip{'ZONE'}" );
		push(@cols, "".($geoip{'DESCRIPTION'} ne '' ? $geoip{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showGroup {
	print &ui_form_start("save_group.cgi", "post" );
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_group.cgi?new=1\">$text{'list_items_create_group'}</a>" );
        @tds = ( "width=1% valign=top",
		 "valign=top",
		 "valign=top",
		 "valign=top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'group'}</b>",
                          "<b>$text{'groupitems'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetGroupList()) {
		my %group = $fw->GetGroup($k);
		local @cols;
		my $href = &ui_link("edit_group.cgi?group=$k",$k);
		push(@cols, "<img src=images/group.png hspace=4>$href" );
		my $grouplist;
		for my $item (@{$group{ITEMS}}) {
			$grouplist .= "$item<br>";
		}
        	push(@cols, $grouplist );
	        push(@cols, "".($group{'DESCRIPTION'} ne '' ? $group{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showTime {
	print &ui_form_start("save_time.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_time.cgi?new=1\">$text{'list_items_create_time'}</a>" );
        @tds = ( "width=1% valign=top",
	 	 "",
		 "",
		 "",
		 "",
		 "" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'time'}</b>",
                          "<b>$text{'weekdays'}</b>",
                          "<b>$text{'timestart'}</b>",
                          "<b>$text{'timestop'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetTimeList()) {
		my %time = $fw->GetTime($k);
		local @cols;
		my $href = &ui_link("edit_time.cgi?time=$k",$k);
		push(@cols, "<img src=images/time.png hspace=4>$href" );
	        push(@cols, "$time{'WEEKDAYS'}" );
	        push(@cols, "$time{'TIMESTART'}" );
	        push(@cols, "$time{'TIMESTOP'}" );
	        push(@cols, "".($time{'DESCRIPTION'} ne '' ? $time{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showTimeGroup {
	print &ui_form_start("save_timegroup.cgi", "post" );
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_timegroup.cgi?new=1\">$text{'list_items_create_timegroup'}</a>" );
        @tds = ( "width=1% valign=top",
		 "valign=top",
		 "valign=top",
		 "valign=top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'timegroup'}</b>",
                          "<b>$text{'timegroupitems'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetTimeGroupList()) {
		my %timegroup = $fw->GetTimeGroup($k);
		local @cols;
		my $href = &ui_link("edit_timegroup.cgi?timegroup=$k",$k);
		push(@cols, "<img src=images/timegroup.png hspace=4>$href" );
		my $timegrouplist;
		for my $item (@{$timegroup{ITEMS}}) {
			$timegrouplist .= "$item<br>";
		}
        	push(@cols, $timegrouplist );
	        push(@cols, "".($timegroup{'DESCRIPTION'} ne '' ? $timegroup{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showHostNameSet {
	print &ui_form_start("save_hostnameset.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_hostnameset.cgi?new=1\">$text{'list_items_create_hostnameset'}</a>" );
        @tds = ( "width=1% valign=top",
		 "valign=top",
		 "valign=top",
		 "valign=top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'hostnameset'}</b>",
                          "<b>$text{'hostnames'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetHostNameSetList()) {
		my %hostnameset = $fw->GetHostNameSet($k);
		local @cols;
		my $href = &ui_link("edit_hostnameset.cgi?hostnameset=$k",$k);
		push(@cols, "<img src=images/hostname.png hspace=4>$href" );
		my $hostnamesetlist;
		for my $hostname (split(/,/, $hostnameset{'HOSTNAMES'})) {
			$hostnamesetlist .= "$hostname<br>";
		}
        	push(@cols, $hostnamesetlist );
	        push(@cols, "".($hostnameset{'DESCRIPTION'} ne '' ? $hostnameset{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showRiskSet {
	print &ui_form_start("save_riskset.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_riskset.cgi?new=1\">$text{'list_items_create_riskset'}</a>" );
        @tds = ( "width=1% valign=top",
		 "",
		 "",
		 "" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'riskset'}</b>",
                          "<b>$text{'risks'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetRiskSetList()) {
		my %riskset = $fw->GetRiskSet($k);
		local @cols;
		my $href = &ui_link("edit_riskset.cgi?riskset=$k",$k);
		push(@cols, "<img src=images/risk.png hspace=4>$href" );
		my $risksetlist;
		for my $i (split(/,/, $riskset{'RISKS'})) {
			my %ndpirisk = $fw->GetNdpiRisk($i);
			$risksetlist .= "$i - $ndpirisk{'DESCRIPTION'}<br>";
		}
		push(@cols, $risksetlist );
		push(@cols, "".($riskset{'DESCRIPTION'} ne '' ? $riskset{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showRateLimit {
	print &ui_form_start("save_ratelimit.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_ratelimit.cgi?new=1\">$text{'list_items_create_ratelimit'}</a>" );
        @tds = ( "width=1% valign=top",
		 "valign=top",
		 "valign=top",
		 "valign=top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'ratelimit'}</b>",
                          "<b>$text{'rate'}</b>",
                          "<b>$text{'description'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetRateLimitList()) {
		my %ratelimit = $fw->GetRateLimit($k);
		local @cols;
		my $href = &ui_link("edit_ratelimit.cgi?ratelimit=$k",$k);
		push(@cols, "<img src=images/rate.png hspace=4>$href" );
        	push(@cols, "$ratelimit{'RATE'} <i>Mbps</i>" );
	        push(@cols, "".($ratelimit{'DESCRIPTION'} ne '' ? $ratelimit{'DESCRIPTION'} : '&nbsp;')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=\"100%\"><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td align="right">'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
