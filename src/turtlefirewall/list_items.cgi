#!/usr/bin/perl

#======================================================================
# Turtle Firewall webmin module
#
# Copyright (c) Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================

do 'turtlefirewall-lib.pl';

&ui_print_header( "$icons{SHIELD}{IMAGE}$text{'list_items_title'}", $text{'title'}, "" );

$form = 0;
&showAddressList();

$form++;
print "<br><br>";
&showZone();

$form++;
print "<br><br>";
&showHost();

$form++;
print "<br><br>";
&showNet();

$form++;
print "<br><br>";
&LoadCountryCodes( $fw );
&showGeoip();

$form++;
print "<br><br>";
&showIPSet();

$form++;
print "<br><br>";
&showGroup();

$form++;
print "<br><br>";
&showHostNameSet();

$form++;
print "<br><br>";
&LoadNdpiRisks( $fw );
&showRiskSet();

$form++;
print "<br><br>";
&showRateLimit();

$form++;
print "<br><br>";
&showTime();

$form++;
print "<br><br>";
&showTimeGroup();

&ui_print_footer('index.cgi',$text{'index'});

#============================================================================

sub showAddressList {
	print &ui_subheading($icons{ADDRESSLIST}{IMAGE},$text{'addresslist'});
	print &ui_form_start("save_addresslist.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_addresslist.cgi?new=1\">$text{'list_items_create_addresslist'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'file'}</b>",
			  "<b>$text{'items'}</b>",
                          "<b>$text{'type'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
        foreach my $b (sort keys %blacklists) {
		local @cols;
		push(@cols, "$icons{BLACKLIST}{IMAGE}<i>$b</i>");
		push(@cols, "$icons{FILE}{IMAGE}$blacklists{$b}{FILE}");
		my $blacklistcount = qx{wc -l < $blacklists{$b}{FILE} 2>/dev/null};
		if( $blacklistcount eq '' ) { $blacklistcount = '0'; }
		push(@cols, $blacklistcount);
		push(@cols, "$icons{OPTION}{IMAGE}$blacklists{$b}{TYPE}" );
		push(@cols, "$icons{DESCRIPTION}{IMAGE}$blacklists{$b}{DESCRIPTION}");
		push(@cols, "".($fw->GetOption("drop_$b") eq 'on' ? "1" : '0')."" );
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
        }
	for my $k ($fw->GetAddressListList()) {
		my %addresslist = $fw->GetAddressList($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_addresslist.cgi?addresslist=$k",$k);
		push(@cols, "$icons{ADDRESSLIST}{IMAGE}$href" );
		push(@cols, "$icons{FILE}{IMAGE}$addresslist{'FILE'}" );
		my $listcount = qx{wc -l < $addresslist{'FILE'} 2>/dev/null};
		if( $listcount eq '' ) { $listcount = '0'; }
		push(@cols, $listcount);
		push(@cols, "$icons{OPTION}{IMAGE}$addresslist{'TYPE'}" );
		push(@cols, "".($addresslist{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$addresslist{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showZone {
	print &ui_subheading($icons{ZONE}{IMAGE},"$text{'zone'}");
	print &ui_form_start("save_zone.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_zone.cgi?new=1\">$text{'list_items_create_zone'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'interface'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetZoneList()) {
		my %zone = $fw->GetZone($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_zone.cgi?zone=$k",$k);
		if( $k eq 'FIREWALL' ) {
			push(@cols, "$icons{FIREWALL}{IMAGE}<i>$k</i>" );
		} else {
			push(@cols, "$icons{ZONE}{IMAGE}$href" );
		}
		push(@cols, "".($zone{'IF'} ne '' ? "$icons{INTERFACE}{IMAGE}$zone{'IF'}" : '&nbsp;')."" );
		push(@cols, "".($zone{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$zone{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showHost {
	print &ui_subheading($icons{HOST}{IMAGE},$text{'host'});
	print &ui_form_start("save_host.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_host.cgi?new=1\">$text{'list_items_create_host'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'hostaddress'}</b>",
                          "<b>$text{'macaddress'}</b>",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetHostList()) {
		my %host = $fw->GetHost($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_host.cgi?host=$k",$k);
		push(@cols, "$icons{HOST}{IMAGE}$href" );
	        push(@cols, "".($host{'IP'} ne '' ? "$icons{ADDRESS}{IMAGE}$host{'IP'}" : '&nbsp;')."" );
	        push(@cols, "".($host{'MAC'} ne '' ? "$icons{ADDRESS}{IMAGE}$host{'MAC'}" : '&nbsp;')."" );
	        push(@cols, "$icons{ZONE}{IMAGE}$host{'ZONE'}" );
	        push(@cols, "".($host{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$host{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showNet {
	print &ui_subheading($icons{NET}{IMAGE},$text{'net'});
	print &ui_form_start("save_net.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_net.cgi?new=1\">$text{'list_items_create_net'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'netaddress'}</b>",
                          "<b>$text{'netmask'}</b>",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetNetList()) {
		my %net = $fw->GetNet($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		push(@cols, $count);
		local @cols;
		my $href = &ui_link("edit_net.cgi?net=$k",$k);
		push(@cols, "$icons{NET}{IMAGE}$href" );
	        push(@cols, "$icons{ADDRESS}{IMAGE}$net{'IP'}" );
	        push(@cols, "$icons{NETMASK}{IMAGE}$net{'NETMASK'}" );
	        push(@cols, "$icons{ZONE}{IMAGE}$net{'ZONE'}" );
	        push(@cols, "".($net{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$net{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showGeoip {
	print &ui_subheading($icons{GEOIP}{IMAGE},$text{'geoip'});
	print &ui_form_start("save_geoip.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_geoip.cgi?new=1\">$text{'list_items_create_geoip'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'countrycode'}</b>",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetGeoipList()) {
		my %geoip = $fw->GetGeoip($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_geoip.cgi?geoip=$k",$k);
		push(@cols, "$icons{GEOIP}{IMAGE}$href" );
		my %g = $fw->GetCountryCode($geoip{'IP'});
		push(@cols, "$icons{COUNTRYCODE}{IMAGE}$geoip{'IP'} - $g{'DESCRIPTION'}" );
	        push(@cols, "$icons{ZONE}{IMAGE}$geoip{'ZONE'}" );
		push(@cols, "".($geoip{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$geoip{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showIPSet {
	print &ui_subheading($icons{IPSET}{IMAGE},$text{'ipset'});
	print &ui_form_start("save_ipset.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_ipset.cgi?new=1\">$text{'list_items_create_ipset'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'addresslist'}</b>",
                          "<b>$text{'zone'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetIPSetList()) {
		my %ipset = $fw->GetIPSet($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_ipset.cgi?ipset=$k",$k);
		push(@cols, "$icons{IPSET}{IMAGE}$href" );
		push(@cols, "$icons{ADDRESS}{IMAGE}$ipset{'IP'}" );
	        push(@cols, "$icons{ZONE}{IMAGE}$ipset{'ZONE'}" );
		push(@cols, "".($ipset{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$ipset{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showGroup {
	print &ui_subheading($icons{GROUP}{IMAGE},$text{'group'});
	print &ui_form_start("save_group.cgi", "post" );
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_group.cgi?new=1\">$text{'list_items_create_group'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'groupitems'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetGroupList()) {
		my %group = $fw->GetGroup($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_group.cgi?group=$k",$k);
		push(@cols, "$icons{GROUP}{IMAGE}$href" );
		my $grouplist;
		my $type = '';
		for my $item (@{$group{ITEMS}}) {
			$type = $fw->GetItemType($item);
			$grouplist .= "$icons{$type}{IMAGE}$item<br>";
		}
        	push(@cols, $grouplist );
	        push(@cols, "".($group{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$group{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showHostNameSet {
	print &ui_subheading($icons{HOSTNAMESET}{IMAGE},$text{'hostnameset'});
	print &ui_form_start("save_hostnameset.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_hostnameset.cgi?new=1\">$text{'list_items_create_hostnameset'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'hostnames'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetHostNameSetList()) {
		my %hostnameset = $fw->GetHostNameSet($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_hostnameset.cgi?hostnameset=$k",$k);
		push(@cols, "$icons{HOSTNAMESET}{IMAGE}$href" );
		my $hostnamesetlist;
		for my $hostname (split(/,/, $hostnameset{'HOSTNAMES'})) {
			$hostnamesetlist .= "$icons{HOSTNAME}{IMAGE}$hostname<br>";
		}
        	push(@cols, $hostnamesetlist );
	        push(@cols, "".($hostnameset{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$hostnameset{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showRiskSet {
	print &ui_subheading($icons{RISKSET}{IMAGE},$text{'riskset'});
	print &ui_form_start("save_riskset.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_riskset.cgi?new=1\">$text{'list_items_create_riskset'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'risks'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetRiskSetList()) {
		my %riskset = $fw->GetRiskSet($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_riskset.cgi?riskset=$k",$k);
		push(@cols, "$icons{RISKSET}{IMAGE}$href" );
		my $risksetlist;
		for my $i (split(/,/, $riskset{'RISKS'})) {
			my %ndpirisk = $fw->GetNdpiRisk($i);
			$risksetlist .= "$icons{RISK}{IMAGE}$i - $ndpirisk{'DESCRIPTION'}<br>";
		}
		push(@cols, $risksetlist );
		push(@cols, "".($riskset{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$riskset{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showRateLimit {
	print &ui_subheading($icons{RATELIMIT}{IMAGE},$text{'ratelimit'});
	print &ui_form_start("save_ratelimit.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_ratelimit.cgi?new=1\">$text{'list_items_create_ratelimit'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'rate'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetRateLimitList()) {
		my %ratelimit = $fw->GetRateLimit($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_ratelimit.cgi?ratelimit=$k",$k);
		push(@cols, "$icons{RATELIMIT}{IMAGE}$href" );
        	push(@cols, "$icons{RATE}{IMAGE}$ratelimit{'RATE'} <i>Mbps</i>" );
	        push(@cols, "".($ratelimit{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$ratelimit{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showTime {
	print &ui_subheading($icons{TIME}{IMAGE},$text{'time'});
	print &ui_form_start("save_time.cgi", "post");
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_time.cgi?new=1\">$text{'list_items_create_time'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
	 	 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'weekdays'}</b>",
                          "<b>$text{'timestart'}</b>",
                          "<b>$text{'timestop'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetTimeList()) {
		my %time = $fw->GetTime($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_time.cgi?time=$k",$k);
		push(@cols, "$icons{TIME}{IMAGE}$href" );
	        push(@cols, "$icons{ITEM}{IMAGE}$time{'WEEKDAYS'}" );
	        push(@cols, "$icons{TIMESTART}{IMAGE}$time{'TIMESTART'}" );
	        push(@cols, "$icons{TIMESTOP}{IMAGE}$time{'TIMESTOP'}" );
	        push(@cols, "".($time{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$time{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
sub showTimeGroup {
	print &ui_subheading($icons{TIMEGROUP}{IMAGE},$text{'timegroup'});
	print &ui_form_start("save_timegroup.cgi", "post" );
	@links = ( &select_all_link("d", $form),
       		   &select_invert_link("d", $form),
		   "<a href=\"edit_timegroup.cgi?new=1\">$text{'list_items_create_timegroup'}</a>" );
        @tds = ( "width=1% style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "style=vertical-align:top",
		 "width=1% style=vertical-align:top" );
        print &ui_columns_start([
			  "",
                          "<b>$text{'name'}</b>",
                          "<b>$text{'timegroupitems'}</b>",
                          "<b>$text{'description'}</b>",
                          "<b>$text{'reference'}</b>" ], 100, 0, \@tds);
	for my $k ($fw->GetTimeGroupList()) {
		my %timegroup = $fw->GetTimeGroup($k);
		my %itemreferences = $fw->GetItemReferences($k);
		my $count = keys %itemreferences;	
		local @cols;
		my $href = &ui_link("edit_timegroup.cgi?timegroup=$k",$k);
		push(@cols, "$icons{TIMEGROUP}{IMAGE}$href" );
		my $timegrouplist;
		for my $item (@{$timegroup{ITEMS}}) {
			$timegrouplist .= "$icons{TIME}{IMAGE}$item<br>";
		}
        	push(@cols, $timegrouplist );
	        push(@cols, "".($timegroup{'DESCRIPTION'} ne '' ? "$icons{DESCRIPTION}{IMAGE}$timegroup{'DESCRIPTION'}" : '&nbsp;')."" );
		my $href = &ui_link("list_itemreferences.cgi?item=$k",$count);
		push(@cols, $href);
		print &ui_checked_columns_row(\@cols, \@tds, "d", $k);
	}
	print &ui_columns_end();
	print "<table width=100%><tr>";
	print '<td>'.&ui_links_row(\@links).'</td>';
	print '<td style=text-align:right>'.&ui_submit( $text{'delete_selected'}, "delete").'</td>';
	print "</tr></table>";
	print &ui_form_end();
}
