#
# TurtleFirewall: Turtle Firewall Library
#
# Software per la configurazione di un firewall linux (iptables)
#
#   2002/02/12 11:27:00
#
#======================================================================
# Copyright (c) 2001-2011 Andrea Frigido
# You may distribute under the terms of either the GNU General Public
# License
#======================================================================
#
# Changelog:
# 1.38 Debian 6.0 Compatibility
#

package TurtleFirewall;

use XML::Parser;

# Turtle Firewall Version
sub Version {
	return '1.38';
}

sub new {
	my $this ={};
	#$this->{NOME} = undef;
	$this->{fw} = ();
	$this->{fwItems} = ();
	$this->{fwKeys} = ();
	$this->{fw_file} = '';
	$this->{fwservices_file} = '';
	$this->{userdef_fwservices_file} = '';
	$this->{log_limit} = undef;
	$this->{log_limit_burst} = undef;
	bless $this;
	return $this
}

##
# Public method for get firewall info (after LoadFirewall)
sub GetZoneList {
	my $this = shift;
	return sort( keys %{ $this->{fw}{ZONE} } );
}
sub GetNetList {
	my $this = shift;
	return sort( keys %{ $this->{fw}{NET} } );
}
sub GetHostList {
	my $this = shift;
	return sort( keys %{ $this->{fw}{HOST} } );
}
sub GetGroupList {
	my $this = shift;
	return @{$this->{fwKeys}{GROUP}};
}
sub GetZone {
	my ($this,$name) = @_;
	return %{ $this->{fw}{ZONE}{$name} };
}
sub GetNet {
	my ($this,$name) = @_;
	return %{ $this->{fw}{NET}{$name} };
}
sub GetHost {
	my ($this,$name) = @_;
	return %{ $this->{fw}{HOST}{$name} };
}
sub GetGroup {
	my ($this,$name) = @_;
	return %{ $this->{fw}{GROUP}{$name} };
}
sub GetAllItemsList {
	my $this = shift;
	return sort( keys %{ $this->{fwItems} } );
}
# GetItemsAllowToGroup( group )
# Get items allow to inserted into the group: all items defined before the group
sub GetItemsAllowToGroup {
	my $this = shift;
	my $group = shift;
	my @items = ();
	push @items, 'FIREWALL';
	push @items, @{$this->{fwKeys}{ZONE}};
	push @items, @{$this->{fwKeys}{NET}};
	push @items, @{$this->{fwKeys}{HOST}};
	foreach my $g ( @{$this->{fwKeys}{GROUP}} ) {
		if( $g eq $group ) {
			last;
		}
		push @items, $g;
	}
	return @items;
}
sub GetServicesList {
	my $this = shift;
	return sort( keys %{ $this->{services} } );
}
sub GetService {
	my $this = shift;
	my $name = shift;
	return %{ $this->{services}{$name} };
}

sub GetMasqueradesCount {
	my $this = shift;
	return $#{$this->{fw}{MASQUERADE}}+1;
}
sub GetMasquerade {
	# param n = id of masquerade rule (1 .. MasqueradeCount)
	my ($this,$n) = @_;
	return %{ $this->{fw}{MASQUERADE}[$n-1] };
}

sub GetNatsCount {
	my $this = shift;
	return $#{$this->{fw}{NAT}}+1;
}
sub GetNat {
	my ($this,$n) = @_;
	return %{ $this->{fw}{NAT}[$n-1] };
}

sub GetRedirectCount {
	my $this = shift;
	return $#{$this->{fw}{REDIRECT}}+1;
}
sub GetRedirect {
	my ($this,$n) = @_;
	return %{ $this->{fw}{REDIRECT}[$n-1] };
}

sub GetRulesCount {
	my $this = shift;
	return $#{$this->{fw}{RULE}}+1;
}
sub GetRule {
	my ($this,$n) = @_;
	return %{ $this->{fw}{RULE}[$n-1] };
}
# Get Firewall Configuration Specific Option
sub GetOption {
	my ($this,$name) = @_;
	return $this->{fw}{OPTION}{$name};
}


# AddGroup( $group, $description, @items );
sub AddGroup {
	my $this = shift;
	my $group = shift;
	my $description = shift;
	my @items = @_;
	if( !$this->{fw}{GROUP}{$group} ) {
		# Se non e' gia' stato inserito lo aggiungo alla lista ordinata di keys
		push @{ $this->{fwKeys}{GROUP} }, $group;
	}
	%{ $this->{fw}{GROUP}{$group} } = ( 'DESCRIPTION'=>$description );
	@{ $this->{fw}{GROUP}{$group}{ITEMS} } = @items;
	$this->{fwItems}{$group} = 'GROUP';
	return 1;
}
# AddHost( $name, $ip, $mac, $zone, $description )
sub AddHost {
	my ($this, $name, $ip, $mac, $zone, $description) = @_;
	%{ $this->{fw}{HOST}{$name} } = ('NAME'=>$name, 'IP'=>$ip, 'MAC'=>$mac, 'ZONE'=>$zone, 'DESCRIPTION'=>$description );
	$this->{fwItems}{$name} = 'HOST';
}
# AddNet( $name, $ip, $netmask, $zone, $description )
sub AddNet {
	my ($this, $name, $ip, $netmask, $zone, $description) = @_;
	%{ $this->{fw}{NET}{$name} } = ('NAME'=>$name, 'IP'=>$ip, 'NETMASK'=>$netmask,'ZONE'=>$zone, 'DESCRIPTION'=>$description );
	$this->{fwItems}{$name} = 'NET';
	return 1;
}
# AddZone( $name, $if, $description  )
sub AddZone {
	my ($this, $name, $if, $description) = @_;
	%{ $this->{fw}{ZONE}{$name} } = ('NAME'=>$name, 'IF'=>$if, 'DESCRIPTION'=>$description );
	$this->{fwItems}{$name} = 'ZONE';
	return 1;
}
# AddMasquerade( $idx, $zone, $active ) if $idx==0 then add new Masquerade
sub AddMasquerade {
	my ($this, $idx, $src, $dst, $service, $port, $masquerade, $active ) = @_;
	
	my %attr = ( 'SRC'=>$src, 'DST'=>$dst, 'SERVICE'=>$service);
	if( $port ne '' ) { $attr{PORT} = $port; }
	if( ! $masquerade ) { $attr{MASQUERADE} = 'NO'; }
	if( ! $active ) { $attr{ACTIVE} = 'NO'; }
	$this->AddMasqueradeAttr( $idx, %attr );
}
sub AddMasqueradeAttr {
	my $this = shift;
	my $idx = shift;
	my %attr = @_;
	if( $idx == 0 ) {
		%{ $this->{fw}{MASQUERADE}[$#{$this->{fw}{MASQUERADE}}+1] } = %attr;
	} else {
		%{ $this->{fw}{MASQUERADE}[$idx-1] } = %attr;
	}
}


# AddNat( $idx, $virtual, $real, $service, $port, $active ) if $idx==0 then add new Masquerade
sub AddNat {
	my ($this, $idx, $virtual, $real, $service, $port, $active) = @_;
	my %attr = ('VIRTUAL'=>$virtual, 'REAL'=>$real);
	if( $service ne '' ) { $attr{SERVICE} = $service; }
	if( $port ne '' ) { $attr{PORT} = $port; }
	if( ! $active ) { $attr{ACTIVE} = 'NO'; }
	$this->AddNatAttr( $idx, %attr );
}
sub AddNatAttr {
	my $this = shift;
	my $idx = shift;
	my %attr = @_;
	if( $idx == 0 ) {
		%{ $this->{fw}{NAT}[$#{$this->{fw}{'NAT'}}+1] } = %attr;
	} else {
		%{ $this->{fw}{NAT}[$idx-1] } = %attr;
	}
}

# AddRedirect( $idx, $src, $dst, $service, $port, $toport, $active );
sub AddRedirect {
	my ($this, $idx, $src, $dst, $service, $port, $toport, $redirect, $active ) = @_;
	my %attr = ( 'SRC'=>$src, 'DST'=>$dst, 'SERVICE'=>$service);
	if( $port ne '' ) { $attr{PORT} = $port; }
	if( $toport ne '' ) { $attr{TOPORT} = $toport; }
	if( ! $redirect ) { $attr{REDIRECT} = 'NO'; }
	if( ! $active ) { $attr{ACTIVE} = 'NO'; }
	$this->AddRedirectAttr( $idx, %attr );
}
sub AddRedirectAttr {
	my $this = shift;
	my $idx = shift;
	my %attr = @_;
	if( $idx == 0 ) {
		%{$this->{fw}{'REDIRECT'}[$#{$this->{fw}{'REDIRECT'}}+1]} = %attr;
	} else {
		%{$this->{fw}{'REDIRECT'}[$idx-1]} = %attr;
	}
}

# AddRule( $idx, $src, $dst, $service, $port, $target, $mark, $active, $description );
sub AddRule {
	my ($this, $idx, $src, $dst, $service, $port, $target, $mark, $active, $description ) = @_;
	my %attr = ( 'SRC'=>$src, 'DST'=>$dst, 'SERVICE'=>$service);
	if( $target ne '' ) { $attr{TARGET} = $target; }
	if( $port ne '' ) { $attr{PORT} = $port; }
	if( $mark ne '' ) { $attr{MARK} = $mark; }
	if( ! $active ) { $attr{ACTIVE} = 'NO'; }
	if( $description ne '' ) { $attr{DESCRIPTION} = $description; }
	$this->AddRuleAttr( $idx, %attr );
}
sub AddRuleAttr {
	my $this = shift;
	my $idx = shift;
	my %attr = @_;
	if( $idx == 0 ) {
		%{$this->{fw}{'RULE'}[$#{$this->{fw}{'RULE'}}+1]} = %attr;
	} else {
		%{$this->{fw}{'RULE'}[$idx-1]} = %attr;
	}
}

sub MoveRule {
	my ($this, $idxSrc, $idxDst) = @_;
	my %attr = %{$this->{fw}{RULE}[$idxSrc-1]};
	splice @{$this->{fw}{RULE}}, $idxSrc-1, 1;
	splice @{$this->{fw}{RULE}}, $idxDst-1, 0, \%attr;
}


# AddOption( $name, $value );
sub AddOption {
	my ($this, $name, $value) = @_;
	$this->{fw}{OPTION}{$name} = $value;
}


# DeleteItem( $name );
sub DeleteItem {
	my $this = shift;
	my $name = shift;
	my $type = $this->{fwItems}{$name};

	# Now I check if this item is included into a group
	my $found = 0;
	for my $g (@{$this->{fwKeys}{GROUP}}) {
		for my $i (@{$this->{fw}{GROUP}{$g}{ITEMS}}) {
			if( $i eq $name ) {
				$found = 1;
				last;
			}
		}
	}

	# Now I check if this item is used by a rule
	my $rules = $this->GetRulesCount();
	for( my $r=0; $r<$rules; $r++ ) {
		my %rule = $this->GetRule( $r );
		if( $rule{SRC} eq $name || $rule{DST} eq $name ) {
			$found = 1;
			last;
		}
	}

	# Now I check if this item is used by a redirect rule
	my $redirectlist = $this->GetRedirectCount();
	for( my $r=0; $r<$redirectlist; $r++ ) {
		my %redirect = $this->GetRedirect( $r );
		if( $redirect{SRC} eq $name || $redirect{DST} eq $name ) {
			$found = 1;
			last;
		}
	}

	# Now I check if this item is used by a NAT rule
	if( $type eq 'HOST' ) {
		my $nats = $this->GetNatsCount();
		for( my $n=0; $n<$nats; $n++ ) {
			my %nat = $this->GetNat( $n );
			if( $nat{VIRTUAL} eq $name || $nat{REAL} eq $name ) {
				$found = 1;
				last;
			}
		}
	}

	# Now I check if this item is used by a masquerade rule
	my $masqs = $this->GetMasqueradesCount();
	for( my $m=0; $m<$masqs; $m++ ) {
		my %masq = $this->GetMasquerade( $m );
		if( $masq{SRC} eq $name || $masq{DST} eq $name ) {
			$found = 1;
			last;
		}
	}
		
	if( !$found ) {
		delete $this->{fw}{$type}{$name};
		delete $this->{fwItems}{$name};
		my @newKeys = ();
		for my $k (@{$this->{fwKeys}{$type}}) {
			if( $k ne $name ) {
				push @newKeys, $k;
			}
		}
		@{$this->{fwKeys}{$type}} = @newKeys;
		return 1;
	} else {
		return 0;
	}
}

sub RenameItem {
	my $this = shift;
	my ($oldname, $newname) = @_;

	if( $oldname eq '' || $newname eq '' || $this->{fwItems}{$newname} ne '' || $newname eq 'FIREWALL' ) {
		# An Item with this name exists
		return 0;
	} else {
		$type = $this->{fwItems}{$oldname};
		%{$this->{fw}{$type}{$newname}} = %{$this->{fw}{$type}{$oldname}};
		$this->{fw}{$type}{$newname}{NAME} = $newname;
		$this->{fwItems}{$newname} = $type;
		delete $this->{fw}{$type}{$oldname};
		delete $this->{fwItems}{$oldname};
		for( my $i=0; $i<=$#{$this->{fwKeys}{$type}}; $i++ ) {
			if( $this->{fwKeys}{$type}[$i] eq $oldname ) {
				$this->{fwKeys}{$type}[$i] = $newname;
			}
		}

		# If it's a zone, I need to change all items that use this zone.
		if( $type eq 'ZONE' ) {
			foreach $k (@{$this->{fwKeys}{HOST}}) {
				if( $this->{fw}{HOST}{$k}{ZONE} eq $oldname ) {
					$this->{fw}{HOST}{$k}{ZONE} = $newname;
				}
			}
			foreach $k (@{$this->{fwKeys}{NET}}) {
				if( $this->{fw}{NET}{$k}{ZONE} eq $oldname ) {
					$this->{fw}{NET}{$k}{ZONE} = $newname;
				}
			}
		}

		# change itme name in groups
		foreach my $group (@{$this->{fwKeys}{GROUP}}) {
			for( my $i=0; $i<=$#{$this->{fw}{GROUP}{$group}{ITEMS}}; $i++ ) {
				if( $this->{fw}{GROUP}{$group}{ITEMS}[$i] eq $oldname ) {
					$this->{fw}{GROUP}{$group}{ITEMS}[$i] = $newname;
				}
			}
		}

		# Change item name in all rules
		foreach my $ruletype ('RULE','NAT','MASQUERADE','REDIRECT') {
			for( my $i=0; $i<=$#{$this->{fw}{$ruletype}}; $i++ ) {
				foreach $field ('SRC','DST','ZONE','VIRTUAL','REAL') {
					if( $this->{fw}{$ruletype}[$i]{$field} eq $oldname ) {
						$this->{fw}{$ruletype}[$i]{$field} = $newname;
					}
				}
			}
		}

		return 1;
	}
}


# DeleteGroup( $group );
sub DeleteGroup {
	my ($this, $group) = @_;
	return $this->DeleteItem( $group );
}
# DeleteHost( $host );
sub DeleteHost {
	my ($this, $host) = @_;
	return $this->DeleteItem( $host );
}
# DeleteHost( $net );
sub DeleteNet {
	my ($this, $net) = @_;
	return $this->DeleteItem( $net );
}
# DeleteZone( $zone );
sub DeleteZone {
	my ($this, $zone) = @_;
	return $this->DeleteItem( $zone );
}

# DeleteMasquerade( $idx );
sub DeleteMasquerade {
	my ($this, $idx) = @_;
	splice( @{$this->{fw}{'MASQUERADE'}}, $idx-1, 1 );
}
# DeleteNat( $idx );
sub DeleteNat {
	my ($this, $idx) = @_;
	splice( @{$this->{fw}{'NAT'}}, $idx-1, 1 );
}
# DeleteRedirect( $idx );
sub DeleteRedirect {
	my ($this, $idx) = @_;
	splice( @{$this->{fw}{'REDIRECT'}}, $idx-1, 1 );
}
# DeleteRule( $idx );
sub DeleteRule {
	my ($this, $idx) = @_;
	splice( @{$this->{fw}{'RULE'}}, $idx-1, 1 );
}
# DeleteOption( $name );
sub DeleteOption {
	my ($this, $name) = @_;
	delete $this->{fw}{OPTION}{$name};
}



#===================================
# Carico le regole del firewall

#==================
# Load Firewall Items and rules.
sub LoadFirewall {
	my $this = shift;
	my $fwFile = shift;

	$this->{fw_file} = $fwFile;

	# Aggiungo il firewall come zona predefinita
	$this->{fwItems}{FIREWALL} = 'ZONE';
	%{$this->{fw}{ZONE}{FIREWALL}} = (NAME=>'FIREWALL');

	my $xml = new XML::Parser( Style=>'Tree' );
	my @tree = @{ $xml->parsefile( $fwFile ) };

	#------
	# Ciclo sui tag di primo livello (firewall)
	for( my $i=0; $i<=$#tree; $i+=2 ) {
		my $name = uc($tree[$i]);
		if ($name eq 'FIREWALL') {
			my @list = @{$tree[$i+1]};
			my %attr = shift @list;

			#------
			# Ciclo sui tag di secondo livello (hosts, groups, rules ecc.)
			for( my $j=0; $j<=$#list; $j+=2 ) {
				my $name2 = uc($list[$j]);
				if( $name2 eq 'ZONE' ) { $this->_LoadFirewallItem( 'ZONE', @{$list[$j+1]} ); }
				if( $name2 eq 'NET' ) { $this->_LoadFirewallItem( 'NET', @{$list[$j+1]} ); }
				if( $name2 eq 'HOST' ) { $this->_LoadFirewallItem( 'HOST', @{$list[$j+1]} ); }
				if( $name2 eq 'GROUP' ) { $this->_LoadFirewallItem( 'GROUP', @{$list[$j+1]} ); }
				if( $name2 eq 'MASQUERADE' ) { $this->_LoadFirewallNat( 'MASQUERADE', @{$list[$j+1]} ); }
				if( $name2 eq 'NAT' ) { $this->_LoadFirewallNat( 'NAT', @{$list[$j+1]} ); }
				if( $name2 eq 'REDIRECT' ) { $this->_LoadFirewallNat( 'REDIRECT', @{$list[$j+1]} ); }
				if( $name2 eq 'RULE' ) { $this->_LoadFirewallRule( @{$list[$j+1]} ); }
				if( $name2 eq 'OPTIONS' ) { $this->_LoadFirewallOptions( @{$list[$j+1]} ); }
			}
		}
	}
}

sub _LoadFirewallItem {
	my $this = shift;

	my $type = shift;
	my @list = @_;

	my %attrs = upperKeys( %{shift @list} );
	my $name = $attrs{'NAME'};

	if( $this->{fwItems}{$name} ne '' ) {
		print STDERR qq~Error: "$name" item is already present.\n~;
	}
	$this->{fwItems}{$name} = $type;
	push @{$this->{fwKeys}{$type}}, $name;
	%{$this->{fw}{$type}{$name}} = %attrs;
	if( $type eq 'GROUP' ) {
		$this->{fw}{'GROUP'}{$name}{ITEMS} = ();
		for( my $j=0; $j<=$#list; $j+=2 ) {
			if( $list[$j] ne '0' ) {
				my %item_attrs = upperKeys( %{ shift @{$list[$j+1]} } );
				my $item = $item_attrs{'NAME'};
				if( $this->{fwItems}{$item} ne '' ) {
					push @{$this->{fw}{'GROUP'}{$name}{ITEMS}}, $item;
				} else {
					print STDERR "Error: $item item of $name group is not defined.\n";
				}
			}
		}
	}
}

###
# Internal method for add NAT, MASQUERADE or REDIRECT to firewall object
sub _LoadFirewallNat {
	my $this = shift;
	my $type = shift;
	my @list = @_;
	#my $name = $list[$i];
	my %attrs = upperKeys( %{shift @list} );
	
	###
	# Backward compatibility with TurtleFirewall < 1.29 configuration file
	if( $type eq 'MASQUERADE' ) {
		if( !$attrs{DST} && $attrs{ZONE} ) {
			$attrs{DST} = $attrs{ZONE};
			delete $attrs{ZONE};
		}
		if( !$attrs{SERVICE} ) {
			$attrs{SERVICE} = 'all';
		}
	}
	
	%{$this->{fw}{$type}[$#{$this->{fw}{$type}}+1]} = %attrs;
}

###
# Internal method for add RULE to firewall object
sub _LoadFirewallRule {
	my $this = shift;
	my @list = @_;
	my %attrs = upperKeys( %{shift @list} );

	my @srcs = split(/,/,$attrs{'SRC'});
	foreach my $src (@srcs) {
		if( $this->{fwItems}{$src} eq '' && $src ne '*' ) {
			print STDERR "Error: rule number ".($#{$this->{fw}{RULE}}+2)." has an invalid source item ($src).\n";
		}
	}

	my @dsts = split(/,/,$attrs{'DST'});
	foreach my $dst (@dsts) {
		if( $this->{fwItems}{$dst} eq '' && $dst ne '*' ) {
			print STDERR "Errore: rule number ".($#{$this->{fw}{RULE}}+2)." has an invalid destination item ($dst).\n";
		}
	}

	%{$this->{fw}{'RULE'}[$#{$this->{fw}{'RULE'}}+1]} = %attrs;
}

###
# Internal method for add OPTIONS to firewall object
#
# XML:
# <options>
#	<option name="option_name" value="option_value"/>
#	<option ...
# </option>
sub _LoadFirewallOptions {
	my $this = shift;
	my @list = @_;

	my %attrs = upperKeys( %{shift @list} );
	for( my $j=0; $j<=$#list; $j+=2 ) {
		if( $list[$j] ne '0' ) {
			my %option_attrs = upperKeys( %{ shift @{$list[$j+1]} } );
			my $name = $option_attrs{'NAME'};
			my $value = $option_attrs{'VALUE'};
			$this->{fw}{OPTION}{$name} = $value;
		}
	}
}




sub LoadServices {
	my $this = shift;
	my $servicesFile = shift;
	my $userdefServicesFile = shift;

	$this->{fwservices_file} = $servicesFile;
	$this->{userdef_fwservices_file} = $userdefServicesFile;

	my $xml = new XML::Parser( Style=>'Tree' );

	foreach $fileName ( ($servicesFile, $userdefServicesFile) ) {
		if( -f $fileName ) {

			my @tree = @{ $xml->parsefile( $fileName ) };

			#------
			# Ciclo sui tag di primo livello (SERVICES)
			for( my $i=0; $i<=$#tree; $i+=2 ) {
				my $name = uc($tree[$i]);
				if ($name eq 'SERVICES') {
					my @list = @{$tree[$i+1]};
					shift @list;

					#------
					# Ciclo sui tag di secondo livello (SERVICE)
					for( my $j=0; $j<=$#list; $j+=2 ) {
						my $name2 = uc($list[$j]);
						if( $name2 eq 'SERVICE' ) {
							my %attrs = upperKeys( %{ shift @{$list[$j+1]} } );
							my @filters = @{$list[$j+1]};

							my $service = $attrs{'NAME'};

							%{ $this->{services}{$service} } = (
								'DESCRIPTION' => $attrs{'DESCRIPTION'},
								'FILTERS' => ()
								);

							for( my $k=0; $k<=$#filters; $k+=2 ) {
								my $name3 = uc( $filters[$k] );
								my %filter = upperKeys( %{shift @{$filters[$k+1]}} );
								if( $name3 eq 'FILTER' ) {
									%{$this->{services}{$service}{FILTERS}[$#{$this->{services}{$service}{FILTERS}}+1]} = %filter;
								}
							}
						}
					}
				}
			}
		}
	}
}

###
# Funzione di servizio.
# Passato un hash come parametro ne converte le chiavi in maiuscolo.
sub upperKeys {
	my %hash = @_;
	my %newHash;
	@ks = keys %hash;
	foreach $k (@ks) {
		$newHash{uc($k)} = $hash{$k};
	}
	return %newHash;
}

sub SaveFirewall {
	my $this = shift;
	$this->SaveFirewallAs( $this->{fw_file} );
}

sub SaveFirewallAs {
	my $this = shift;
	my ($fwFile) = @_;

	my %fw = %{ $this->{fw} };

	my $xml = "<firewall>\n";

	$xml .= "\n";
	$xml .= "<options>\n";
	foreach my $k (keys %{$fw{'OPTION'}}) {
		$xml .= $this->attr2xml( 'option', ('name'=>$k, 'value'=>$fw{'OPTION'}{$k}) );
	}
	$xml .= "</options>\n";

	$xml .= "\n";
	foreach my $k (keys %{$fw{'ZONE'}}) {
		if( $k ne 'FIREWALL' ) {
			$xml .= $this->attr2xml( 'zone', %{$fw{'ZONE'}{$k}} );
		}
	}
	$xml .= "\n";
	foreach my $k (keys %{$fw{'NET'}}) {
		$xml .= $this->attr2xml( 'net', %{$fw{'NET'}{$k}} );
	}
	$xml .= "\n";
	foreach my $k (keys %{$fw{'HOST'}}) {
		$xml .= $this->attr2xml( 'host', %{$fw{'HOST'}{$k}} );
	}
	$xml .= "\n";
	#foreach my $k (keys %{$fw{'GROUP'}}) {
	foreach my $k (@{$this->{fwKeys}{GROUP}}) {
		$xml .= "<group name=\"$k\" description=\"".$this->_clean($fw{'GROUP'}{$k}{DESCRIPTION})."\">\n";
		foreach my $item (@{$fw{'GROUP'}{$k}{ITEMS}}) {
			$xml .= "\t<item name=\"".$this->_clean($item)."\"/>\n";
		}
		$xml .= "</group>\n";
	}
	$xml .= "\n";
	my @nats = @{$fw{'NAT'}};
	for my $i (0..$#nats) {
		$xml .= $this->attr2xml( 'nat', %{$nats[$i]} );
	}
	$xml .= "\n";
	my @masq = @{$fw{'MASQUERADE'}};
	for my $i (0..$#masq) {
		$xml .= $this->attr2xml( 'masquerade', %{$masq[$i]} );
	}
	$xml .= "\n";
	my @redirectlist = @{$fw{'REDIRECT'}};
	for my $i (0..$#redirectlist) {
		$xml .= $this->attr2xml( 'redirect', %{$redirectlist[$i]} );
	}
	$xml .= "\n";
	my @rules = @{$fw{'RULE'}};
	for my $i (0..$#rules) {
		$xml .= $this->attr2xml( 'rule', %{$rules[$i]} );
	}
	$xml .= "\n";
	$xml .= "</firewall>\n";

	open( FWFILE, ">$fwFile" );
	print FWFILE $xml;
	close( FWFILE );
}
sub attr2xml {
	my $this = shift;
	my ($tag, %attr, @order) = @_;
	my $appo = "<$tag";
	foreach my $k (keys %attr) {
		$appo .= ' '.lc($k).'="'.$this->_clean($attr{$k}).'"';
	}
	$appo .= "/>\n";
	return $appo;
}
# Translate """ to "'", "<" to "&lt;" and ">" to "&gt;" and "&" to "&amp;"
sub _clean {
	my $this = shift;
	my $s = shift;
	$s =~ s/\"/\'/g;
	$s =~ s/\</&lt;/g;
	$s =~ s/\>/&gt;/g;
	$s =~ s/\&/&amp;/g;
	return $s;
}

###
# Check if a name is correct (use only [a-zA-Z0-9\_\-])
sub checkName {
	my $this = shift;
	my $name = shift;
	return $name =~ /^[a-zA-Z0-9\_\-]*$/;
}


# Return the status of firewall (1 = 0n, 0 = off)
sub GetStatus {
	my $iptables = qx{iptables -L -n};
	return $iptables =~ /Chain BACK/g;
}


sub startFirewall {
	my $this = shift;
	
	# PreLoad modules for ftp connections and NAT
	$this->command('modprobe ip_tables', '/dev/null');
	$this->command('modprobe ip_conntrack', '/dev/null');
	$this->command('modprobe ip_conntrack_ftp', '/dev/null');
	$this->command('modprobe ip_nat_ftp', '/dev/null');
		
	# Abilitiamo l'IP forwarding
	$this->command('echo "1"', '/proc/sys/net/ipv4/ip_forward');
	
	if( $this->{fw}{OPTION}{rp_filter} eq 'unchange' ) {
		print "rp_filter: unchange\n";
	} else {
		my $flag;
		if( $this->{fw}{OPTION}{rp_filter} eq 'off' ) {
			print "rp_filter: off\n";
			$flag = 0;
		} else {
			print "rp_filter: on\n";
			$flag = 1;
		}
		$this->command( "for f in /proc/sys/net/ipv4/conf/*/rp_filter; do echo $flag > \$f; done" );
	}

	if( $this->{fw}{OPTION}{log_martians} eq 'unchange' ) {
		print "log_martians: unchange\n";
	} else {
		my $flag;
		if( $this->{fw}{OPTION}{log_martians} eq 'off' ) {
			print "log_martians: off\n";
			$flag = 0;
		} else {
			print "log_martians: on\n";
			$flag = 1;
		}
		$this->command( "for f in /proc/sys/net/ipv4/conf/*/log_martians; do echo $flag > \$f; done" );
	}
	
	###
	# I want ever icmp_echo_ignore_all set to off. Turtle Firewall use iptables
	# rules for drop or allow icmp echo packets. Andrea Frigido 2004-07-17
	$this->command( 'echo "1"', '/proc/sys/net/ipv4/icmp_echo_ignore_broadcasts' );
	$this->command( 'echo "0"', '/proc/sys/net/ipv4/icmp_echo_ignore_all' );
	
	###
	# Disable tcp_ecn flag.
	$this->command( 'echo 0', '/proc/sys/net/ipv4/tcp_ecn' );

	# Don't accept source routed packets. Attackers can use source routing to generate
	# traffic pretending to be from inside your network, but which is routed back along
	# the path from which it came, namely outside, so attackers can compromise your
	# network. Source routing is rarely used for legitimate purposes.
	$this->command( 'for f in /proc/sys/net/ipv4/conf/*/accept_source_route; do echo 0 > $f; done' );

	# Disable ICMP redirect acceptance. ICMP redirects can be used to alter your routing
	# tables, possibly to a bad end.
	$this->command( 'for f in /proc/sys/net/ipv4/conf/*/accept_redirects; do echo 0 > $f; done' );

	# Enable bad error message protection.
	$this->command( 'echo 1', '/proc/sys/net/ipv4/icmp_ignore_bogus_error_responses' );
	
	####
	# Other options
	if( $this->{fw}{OPTION}{ip_conntrack_max} > 0 ) {
		open( FILE, ">/proc/sys/net/ipv4/ip_conntrack_max" );
		print FILE $this->{fw}{OPTION}{ip_conntrack_max};
		close FILE;
		print "ip_conntrack_max: ",$this->{fw}{OPTION}{ip_conntrack_max},"\n";
	}

	my $rules = $this->getIptablesRules();
	
	my $use_iptables_restore = 1;
	
	if( $use_iptables_restore ) {
		umask 0077;
		open FILE, ">/etc/turtlefirewall/iptables.dat";
		print FILE $rules;
		close FILE;
		print "run iptables-restore\n";
		if( -x '/sbin/iptables-restore' ) {
			$this->command('cat /etc/turtlefirewall/iptables.dat | /sbin/iptables-restore');
		} elsif( -x '/usr/sbin/iptables-restore' ) {
			$this->command('cat /etc/turtlefirewall/iptables.dat | /usr/sbin/iptables-restore');	
		} else {
			print STDERR "Error: iptables-restore needed\n";
		}
		# doesn't unlink, for debugging
		#unlink "/etc/turtlefirewall/iptables.dat";
	} else {	
		$this->iptables_restore_emu( $rules );
	}

}

sub stopFirewall {
	my $this = shift;
	#
	# Stop the firewall, allow all connections.
	#
	$this->command(
		"iptables -F; ".
		"iptables -X; ".
		"iptables -t nat -F; ".
		"iptables -t nat -X; ".
		"iptables -P INPUT ACCEPT; ".
		"iptables -P OUTPUT ACCEPT; ".
		"iptables -P FORWARD ACCEPT" );
	# enable ping
	$this->command( 'echo "0"', '/proc/sys/net/ipv4/icmp_echo_ignore_all' );
}

###
# 
sub getIptablesRules {
	my $this = shift;
	
	my $chains = '';
	my $rules = '';
	
	my $mangle_chains = '';
	my $mangle_rules = '';
	
	my $log_limit=60;
	my $log_limit_burst=5;
	if( $this->{fw}{OPTION}{log_limit} > 0 ) {
		$log_limit = $this->{fw}{OPTION}{log_limit};
		print "log_limit: $log_limit\n";
	}
	if( $this->{fw}{OPTION}{log_limit_burst} > 0 ) {
		$log_limit_burst = $this->{fw}{OPTION}{log_limit_burst};
		print "log_limit_burst: $log_limit_burst\n";
	}
	$this->{log_limit} = $log_limit;
	$this->{log_limit_burst} = $log_limit_burst;
	
	$chains .= "*filter\n";
	$chains .= ":FORWARD DROP [0:0]\n";
	$chains .= ":INPUT DROP [0:0]\n";
	$chains .= ":OUTPUT DROP [0:0]\n";

	# Chains for mangle table
	$mangle_chains .= "*mangle\n".
			":PREROUTING ACCEPT [0:0]\n".
			":INPUT ACCEPT [0:0]\n".
			":FORWARD ACCEPT [0:0]\n".
			":OUTPUT ACCEPT [0:0]\n".
			":POSTROUTING ACCEPT [0:0]\n";
	
	# abilito l'accesso da/verso l'interfaccia lo.
	$rules .= "-A INPUT -i lo -j ACCEPT\n";
	$rules .= "-A OUTPUT -o lo -j ACCEPT\n";

	### Log invalid packets then drop packets
	$chains .= ":INVALID - [0:0]\n";
	$chains .= ":CHECK_INVALID - [0:0]\n";
	
	###
	# Deprecated (doesn't work with kernel 2.6,x)
	#print "drop_unclean: ";
	#if( $this->{fw}{OPTION}{drop_unclean} eq 'on' ) {
	#	# 13-09-2002 It doesn't work, wait stable version of unclean module (Andrea Frigido)
	#	# This next rule is marked experimental but does not appear to block legitimite traffic
	#	$rules .= "-A CHECK_INVALID -m unclean -j INVALID\n";
	#	$rules .= "-A INVALID -m unclean ".
	#		" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID unclean:\"\n";
	#	print "on\n";
	#} else {
	#	print "off\n";
	#}
	
	print "drop_invalid_state: ";
	if( $this->{fw}{OPTION}{drop_invalid_state} ne 'off' ) {
		$rules .= "-A CHECK_INVALID -m state --state INVALID -j INVALID\n";
		$rules .= "-A INVALID -m state --state INVALID ".
			" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID STATE:\"\n";
		print "on\n";
	} else {
		print "off\n";
	}
	
	print "drop_invalid_all: ";
	if( $this->{fw}{OPTION}{drop_invalid_all} ne 'off' ) {
		$rules .= "-A CHECK_INVALID -p tcp --tcp-flags ALL ALL -j INVALID\n";
		$rules .= "-A INVALID -p tcp --tcp-flags ALL ALL ".
			" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID ALL:\"\n";
		print "on\n";
	} else {
		print "off\n";
	}
	
	print "drop_invalid_none: ";
	if( $this->{fw}{OPTION}{drop_invalid_none} ne 'off' ) {
		$rules .= "-A CHECK_INVALID -p tcp --tcp-flags ALL NONE -j INVALID\n";
		$rules .= "-A INVALID -p tcp --tcp-flags ALL NONE ".
			" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID NONE:\"\n";
		print "on\n";
	} else {
		print "off\n";
	}
	
	print "drop_invalid_fin_notack: ";
	if( $this->{fw}{OPTION}{drop_invalid_fin_notack} ne 'off' ) {
		$rules .= "-A CHECK_INVALID -p tcp --tcp-flags FIN,ACK FIN -j INVALID\n";
		$rules .= "-A INVALID -p tcp --tcp-flags FIN,ACK FIN ".
			" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID FIN,!ACK:\"\n";
		print "on\n";
	} else {
		print "off\n";
	}
	
	print "drop_invalid_sys_fin: ";
	if( $this->{fw}{OPTION}{drop_invalid_syn_fin} ne 'off' ) {
		$rules .= "-A CHECK_INVALID -p tcp --tcp-flags SYN,FIN SYN,FIN -j INVALID\n";
		$rules .= "-A INVALID -p tcp --tcp-flags SYN,FIN SYN,FIN ".
			" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID SYN,FIN:\"\n";
		print "on\n";
	} else {
		print "off\n";
	}

	print "drop_invalid_syn_rst: ";
	if( $this->{fw}{OPTION}{drop_invalid_syn_rst} ne 'off' ) {
		$rules .= "-A CHECK_INVALID -p tcp --tcp-flags SYN,RST SYN,RST  -j INVALID\n";
		$rules .= "-A INVALID -p tcp --tcp-flags SYN,RST SYN,RST ".
			" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID SYN,RST:\"\n";
		print "on\n";
	} else {
		print "off\n";
	}
	
	print "drop_invalid_fragment: ";
	if( $this->{fw}{OPTION}{drop_invalid_fragment} ne 'off' ) {
		$rules .= "-A CHECK_INVALID -f -j INVALID\n";
		$rules .= "-A INVALID -f ".
			" -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID fragment:\"\n";
		print "on\n";
	} else {
		print "off\n";
	}

	$rules .= "-A CHECK_INVALID -j RETURN\n";
	# Log all invalid then drop
	$rules .= "-A INVALID -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW INVALID PACKET:\"\n";
	$rules .= "-A INVALID -j DROP\n";

	$rules .= "-A INPUT -j CHECK_INVALID\n";
	$rules .= "-A OUTPUT -j CHECK_INVALID\n";
	$rules .= "-A FORWARD -j CHECK_INVALID\n";
	# END of INVALID Packets filter by Mark Francis
	############################################
	
	# Definizione della catena di ritorno
	# Chain dei pacchetti di ritorno (NO nuove connessioni)
	$chains .= ":BACK - [0:0]\n";
	$rules .= "-A BACK -m state --state ESTABLISHED,RELATED -j ACCEPT\n";
	$rules .= "-A BACK -j RETURN\n";

	# Definizione della catena ICMP-ACC
	# Chain per la gestione degli errori standard ICMP
	$chains .= ":ICMP-ACC - [0:0]\n";
	$rules .= "-A ICMP-ACC -p icmp --icmp-type destination-unreachable -j ACCEPT\n";
	$rules .= "-A ICMP-ACC -p icmp --icmp-type source-quench -j ACCEPT\n";
	$rules .= "-A ICMP-ACC -p icmp --icmp-type time-exceeded -j ACCEPT\n";
	$rules .= "-A ICMP-ACC -p icmp --icmp-type parameter-problem -j ACCEPT\n";
	$rules .= "-A ICMP-ACC -j RETURN\n";

	
	# Creo le catene delle ZONE
	my @zone = $this->GetZoneList();
	for(my $i=0; $i<=$#zone; $i++ ) {
		my $z1 = $zone[$i];
		my %zone1 = $this->GetZone($z1);
		for($j=0; $j<=$#zone; $j++ ) {
			my $z2 = $zone[$j];
			my %zone2 = $this->GetZone($z2);
			if( $z1 eq 'FIREWALL' || $z2 eq 'FIREWALL' ) {
				# Definisco le catene per i pacchetti che hanno come destinazione od
				# origine lo stesso firewall.
				# Notare che escludo la coppia FIREWALL -> FIREWALL
				if( $z1 eq 'FIREWALL' && $z2 ne 'FIREWALL' ) {
					$chains .= ":$z1-$z2 - [0:0]\n";
					$rules .= "-A OUTPUT -o \"".$zone2{'IF'}."\" -j $z1-$z2\n";
					$mangle_chains .= ":$z1-$z2 - [0:0]\n";
					$mangle_rules .= "-A OUTPUT -o \"".$zone2{'IF'}."\" -j $z1-$z2\n";
				}
				if( $z1 ne 'FIREWALL' && $z2 eq 'FIREWALL' ) {
					$chains .= ":$z1-$z2 - [0:0]\n";
					$rules .= "-A INPUT -i ".$zone1{'IF'}." -j $z1-$z2\n";
					$mangle_chains .= ":$z1-$z2 - [0:0]\n";
					$mangle_rules .= "-A INPUT -i ".$zone1{'IF'}." -j $z1-$z2\n";
				}
			} else {
				$chains .= ":$z1-$z2 - [0:0]\n";
				$rules .= "-A FORWARD -i ".$zone1{'IF'}." -o ".$zone2{'IF'}." -j $z1-$z2\n";
				$mangle_chains .= ":$z1-$z2 - [0:0]\n";
				$mangle_rules .= "-A FORWARD -i ".$zone1{'IF'}." -o ".$zone2{'IF'}." -j $z1-$z2\n";
			}
		}
	}
	
	# MASQUERADE (sempre dopo il NAT)
	#my $chains_nat = "#=====================================\n".
	#		"# NAT\n".
	my $chains_nat = "*nat\n".
			":PREROUTING ACCEPT [0:0]\n".
			":POSTROUTING ACCEPT [0:0]\n".
			":OUTPUT ACCEPT [0:0]\n";
	my $rules_nat = '';
	for( my $i=1; $i <= $this->GetNatsCount(); $i++ ) {
		$rules_nat .= $this->applyNat( $this->GetNat($i) );
	}

	# MASQUERADE (sempre dopo il NAT)
	#$chains_nat .= "#=====================================\n".
	#		"# Masquerading\n";
	my $masqueradesCount = $this->GetMasqueradesCount();
	if( $masqueradesCount > 0 ) {
		# Add MASQ chain
		$chains_nat .= ":MASQ - [0:0]\n";
		$rules_nat .= "-A POSTROUTING -j MASQ\n";
		for( my $i=1; $i <= $masqueradesCount; $i++ ) {
			$rules_nat .= $this->applyMasquerade( $this->GetMasquerade($i) );
		}
		# close the MASQ chain with a RETURN to the POSTROUTING parent chain
		$rules_nat .= "-A MASQ -j RETURN\n";
	}
	
	# REDIRECT
	#$chains_nat .= "#=====================================\n".
	#		"# REDIRECT\n";
	my $redirectCount = $this->GetRedirectCount();
	if( $redirectCount > 0 ) {
		# Add REDIR chain
		$chains_nat .= ":REDIR - [0:0]\n";
		$rules_nat .= "-A PREROUTING -j REDIR\n";
		for( my $i=1; $i <= $redirectCount; $i++ ) {
			$rules_nat .= $this->applyRedirect( $this->GetRedirect($i) );
		}
		# close the REDIR chain with a RETURN to the PREROUTING parent chain
		$rules_nat .= "-A REDIR -j RETURN\n";
	}

	# Applicazione delle RULEs
	#$rules .= "#=====================================\n".
	#	"# Regole di forwarding.\n";
	my $rulesCount = $this->GetRulesCount();
	my $mangle_specrules = ''; 
	for( my $i=1; $i <= $rulesCount; $i++ ) {
		$rules .= $this->applyRule( 1, 0, $this->GetRule($i) );
		$mangle_specrules .= $this->applyRule( 0, 1, $this->GetRule($i) );
	}

	# chiudo le catene delle zone
	#$rules .= "#=====================================\n".
	#	"# Chiusura di tutte le catene con relativo log\n";
	for(my $i=0; $i<=$#zone; $i++ ) {
		$z1 = $zone[$i];
		for($j=0; $j<=$#zone; $j++ ) {
			$z2 = $zone[$j];
			if( $z1 ne 'FIREWALL' || $z2 ne 'FIREWALL' ) {
				my $logprefix = "TFW $z1-$z2";
				if( length($logprefix) > 28 ) {
					# iptables need log-prefix strings up to 29 chars length (with char ":")
					$logprefix = substr( $logprefix, 0, 28 );
				}
				#comment( "# Chiusura catena $z1 -> $z2" );
				$rules .= "-A $z1-$z2 -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"$logprefix:\"\n";
				$rules .= "-A $z1-$z2 -j DROP\n";
			}
		}
	}
	for my $chain (('INPUT','OUTPUT','FORWARD')) {
		$rules .= "-A $chain -m limit --limit $log_limit/hour --limit-burst $log_limit_burst -j LOG --log-prefix \"TFW $chain:\"\n";
	}
	print "DENY any other connections\n";
	
	return ($mangle_specrules ? $mangle_chains.$mangle_rules.$mangle_specrules."COMMIT\n" : "*mangle\nCOMMIT\n").
		$chains.$rules."COMMIT\n".$chains_nat.$rules_nat."COMMIT\n";
}


sub applyNat {
	my $this = shift;
	my %nat = @_;

	my %fw = %{$this->{fw}};
	my %fwItems = %{$this->{fwItems}};
	my %services = %{$this->{services}};

	my $rules = '';
	
	if( $nat{ACTIVE} eq 'NO' ) {
		return '';
	}

	my $virtual	= $nat{VIRTUAL};
	my $real	= $nat{REAL};
	my $nmService	= $nat{SERVICE};
	my $port	= $nat{PORT};			# Optional port identifier
	my $virtual_ip='';
	my $virtual_if='';
	my $real_ip='';

	# service is a list of services?
	if( $nmService =~ /,/ ) {
		my @services = split( /,/, $nmService );
		my %newnat = %nat;
		foreach my $serv (@services) {
			$newnat{SERVICE} = $serv;
			$rules .= $this->applyNat( %newnat );
		}
		return $rules;
	}

	if( $virtual eq '' ) {
		print STDERR "Error: VIRTUAL attribute missing in NAT rule definition.\n";
		return $rules;
	}
	if( $real eq '' ) {
		print STDERR "Error: REAL attribute missing in NAT rule definition.\n";
		return $rules;
	}

	if( $fwItems{$virtual} ne 'HOST' && $fwItems{$virtual} ne 'ZONE' ) {
		print STDERR "Error: in a NAT rule definition, VIRTUAL attribute [$virtual] is not a valid host or zone name.\n";
		return $rules;
	}
	if( $fwItems{$virtual} eq 'HOST' ) {
		$virtual_ip = $fw{HOST}{$virtual}{IP};
	}
	if( $fwItems{$virtual} eq 'ZONE' ) {
		$virtual_if = $fw{ZONE}{$virtual}{IF};
	}

	if( $fwItems{$real} ne 'HOST' ) {
		print STDERR "Error: in a NAT rule definition, REAL attribute is not a valid host name.\n";
		return $rules;
	}
	$real_ip = $fw{HOST}{$real}{IP};

	if( $nmService eq '' || $nmService eq 'all' ) {
		# Interface-wide nat. This was the only way natting was used to be.
		if( $virtual_ip ne '' ) {
			# Virtual HOST to Real HOST nat
			print "NAT virtual( $virtual ) --> real( $real )\n";
			#command( "#NAT virtual( $virtual ) -to-> real( $real )" );
			$rules .= "-A PREROUTING -d $virtual_ip -j DNAT --to-destination $real_ip\n";
			# Nat for firewall itself
			$rules .= "-A OUTPUT -d $virtual_ip -j DNAT --to-destination $real_ip\n";
			# Source NAT
			$rules .= "-A POSTROUTING -s $real_ip -j SNAT --to-source $virtual_ip\n";
		} else {
			# ZONE interface to Real HOST nat
			print "NAT from zone( $virtual ) --> real( $real )\n";
			#command( "#NAT from zone ( $virtual ) -to-> real( $real )" );
			$rules .= "-A PREROUTING -i $virtual_if -j DNAT --to-destination $real_ip\n";
			$rules .= "-A POSTROUTING -s $real_ip -o $virtual_if -j MASQUERADE\n";
			# In this case I can't make NAT for firewall itself becouse I can't use -i option
			# with OUTPUT chain
		}
	} else {
		# Service-wide nat. This was introduced with v0.98.
		# On the 'go' way of the specified service we do a DNAT from $virtual_ip:$dport
		# to $real_ip:$dport, while on the 'back' way we do a SNAT from $real_ip:$sport
		# to $virtual_ip:$sport. $state conditions and $jump tags are added to the iptable
		# entries as well.
		
		print "NAT virtual( $virtual ) --> real( $real ) on service( $nmService".
				($port ne '' ? "($port)" : '')." )\n";
		#$rules .= "#NAT virtual( $virtual ) -to-> real( $real ) on service( $nmService($port) )\n";

		# Outputs a nat roule for each defined service channel
		foreach my $filter (@{$services{$nmService}{FILTERS}}) {
			my $direction	= $filter->{DIRECTION};
			my $proto	= $filter->{P};
			my $icmptype	= $filter->{ICMPTYPE};
			my $sport	= $filter->{SPORT};
			my $dport	= $filter->{DPORT};
			my $state	= $filter->{STATE};

			# Fetches
			if( $sport eq 'PORT' ) { $sport = $port; }
			if( $dport eq 'PORT' ) { $dport = $port; }

			# Basic command skeleton
			my $cmd = '';
			$cmd .= (
				$direction eq 'go' ?
					( $virtual_ip ne '' ?
						"-A PREROUTING -d $virtual_ip "
					:
						"-A PREROUTING -i $virtual_if "
					)
				:
					"-A POSTROUTING -s $real_ip "
			);

			# Add protocol filter if the service defines it
			if( $proto eq 'tcp' || $proto eq 'udp' ) {
				$cmd .= "-p $proto ";
				#$cmd .= ( $direction eq 'go' ? "--dport $dport " : "--sport $sport " );
				if( $dport ne '' ) { $cmd .= "--dport $dport "; }
				if( $sport ne '' ) { $cmd .= "--sport $sport "; }
			} elsif( $proto ne 'icmp' ) {
				# Well, I'm coding this... But what purpouse is supposed
				# to have an icmp nat? Mmmmm...
				$cmd .= "-p $proto ";

				if( $icmptype ne '' ) {
					$cmd .= "--icmp-type $icmptype ";
				}
			} elsif( $proto ne '' ) {
				print "  a nat on protocol \"$proto\" had been disregarded.\n";
				next;
			}

			# Add state-related rule
			if( $state ne '' ) {
				$cmd .= "-m state --state $state ";
			}

			# Destination/source mangling
			$cmd .= (
				$direction eq 'go' ?
					"-j DNAT --to-destination $real_ip"
				:
					( $virtual_ip ne '' ?
						"-j SNAT --to-source $virtual_ip"
					:
						"-o $virtual_if -j MASQUERADE"
					)
			);

			# Finally, executes the command
			$rules .= "$cmd\n";

			# If is possible, now I apply the same rule to firewall itself
			if( $cmd =~ /PREROUTING/ && $cmd !~ / -i / ) {
				$cmd =~ s/PREROUTING/OUTPUT/;
				$rules .= "$cmd\n";
			}
		}
	}
	return $rules;
}

# Applica una regola di mascheramento
sub applyMasquerade {
	my $this = shift;
	my %masq = @_;
	
	my %fw = %{$this->{fw}};
	my %fwItems = %{$this->{fwItems}};
	my %services = %{$this->{services}};

	my $rules = '';

	if( $masq{ACTIVE} eq 'NO' ) {
		return '';
	}
	
	# Masquerade or don't masquerade?
	my $is_masquerade = $masq{MASQUERADE} ne 'NO';

	my $src = $masq{SRC};
	my $dst = $masq{DST};
	
	###
	# Backward compatibility with TurtleFirewall < 1.29
	if( !$dst && $masq{ZONE} ) {
		$dst = $masq{ZONE};
	}

	if( $dst eq '' ) {
		print STDERR "Error: DST or ZONE attribute missing in MASQUERADE rule.";
		return $rules;
	}

	#if( $fwItems{$zone} ne 'ZONE' ) {
	#	print STDERR "Error: invalid ZONE attribute missing in MASQUERADE rule.";
	#	return
	#}

	# Vedo se come sorgente ho un group
	if( $fwItems{$src} eq 'GROUP' ) {
		my %newmasq = %masq;
		foreach my $item ( @{$fw{GROUP}{$src}{ITEMS}} ) {
			if( $item ne 'FIREWALL' ) {
				$newmasq{SRC} = $item;
				$rules .= $this->applyMasquerade( %newmasq );
			}
		}
		return $rules;
	}

	# Vedo se come destinazione ho un group
	if( $fwItems{$dst} eq 'GROUP' ) {
		my %newmasq = %masq;
		foreach my $item ( @{$fw{GROUP}{$dst}{ITEMS}} ) {
			if( $item ne 'FIREWALL' ) {
				$newmasq{DST} = $item;
				$rules .= $this->applyMasquerade( %newmasq );
			}
		}
		return $rules;
	}
	
	# Definisco il SERVICE
	my $service = $masq{SERVICE};
	my $port = $masq{PORT};

	# service is a list of services?
	if( $service =~ /,/ ) {
		my @services = split( /,/, $service );
		my %newmasq = %masq;
		foreach my $serv (@services) {
			$newmasq{SERVICE} = $serv;
			$rules .= $this->applyMasquerade( %newmasq );
		}
		return $rules;
	}

	if( $service eq '' ) {
		$service = 'all';
	}

	my ($src_zone, $src_peer, $src_mac) = $this->expand_item( $src );
	my %src_zone_attr = $this->GetZone( $src_zone );
	$src_if = $src_zone_attr{IF};
	my ($dst_zone, $dst_peer) = $this->expand_item( $dst );
	my %dst_zone_attr = $this->GetZone( $dst_zone );
	$dst_if = $dst_zone_attr{IF};
	
	print $is_masquerade ? '' : 'NOT ',"MASQUERADE ( service $service";
	if( $service eq 'tcp' || $service eq 'udp' ) { print "($port)"; }
	print $src ? " $src" : ' *';
	if( $src_mac ne '' ) { print "(mac:$src_mac)"; }
	print " --> $dst ) IF $dst_if\n";
	
	$rules .= $this->applyServiceMasquerade( \%services, $service, $src_if, $src_peer, $src_mac, $dst_if, $dst_peer, $port, $is_masquerade);
	return $rules;
}

sub applyServiceMasquerade {
	my $this = shift;
	my %calledServices = ();
	return $this->_applyServiceMasquerade( \%calledServices, @_ );
}

sub _applyServiceMasquerade {
	my $this = shift;
	my ($ref_calledServices, $ref_services, $serviceName, $src_if, $src_peer, $src_mac, $dst_if, $dst_peer, $port, $is_masquerade) = @_;
	
	my %service = %{$ref_services->{$serviceName}};

	# commento del servizio
	#comment( "# $serviceName: ".$service{DESCRIPTION} );

	$ref_calledServices->{$serviceName} = 1;

	my $rules = '';
	
	# ciclo sulle regole di filering
	my $i;
	for( $i = 0; $i <= $#{$service{FILTERS}}; $i++ ) {

		my %filter = %{$service{FILTERS}[$i]};

		if( $filter{SERVICE} ne '' && !$ref_calledServices->{$filter{SERVICE}} ) {
			# It is a subservice, recursion call to _applyServiceMasquerade
			$rules .= $this->_applyServiceMasquerade( $ref_calledServices, $ref_services, $filter{SERVICE},
				$src_if, $src_peer, $src_mac, $dst_if, $dst_peer, $port, $is_masquerade );
			next;
		}

		my $direction = $filter{DIRECTION};
		my $p = $filter{P};
		my $icmptype = $filter{ICMPTYPE};
		my $sport = $filter{SPORT};
		my $dport = $filter{DPORT};
		my $state = $filter{STATE};
		my $jump = $filter{JUMP};

		if( $direction ne 'go' ) {
			# Don't process Back filters, masquerade is apply only for go direction
			next;
		}

		# porta impostata dalla regola del firewall
		if( $sport eq 'PORT' ) {
			$sport = $port;
		}
		if( $dport eq 'PORT' ) {
			$dport = $port;
		}

		my $cmd='';
		if( $direction eq 'go' && ($jump eq '' || $jump eq 'ACCEPT') ) { 
			$cmd = "-A MASQ ";
			if( $src_if ne '' ) { $cmd .= "-i $src_if "; }
			if( $src_peer && $src_peer ne '0.0.0.0/0' ) { $cmd .= "-s $src_peer "; }
			if( $src_mac =~ /^[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}$/ ) {
				$cmd .= "-m mac --source-mac $src_mac ";
			}
			if( $dst_if ne '' ) { $cmd .= "-o $dst_if "; }
			if( $dst_peer ne '0.0.0.0/0' ) { $cmd .= "-d $dst_peer "; }
			if( $p ne '' ) { $cmd .= "-p $p "; }
			if( $sport ne '' ) { $cmd .= "--sport $sport "; }
			if( $dport ne '' ) { $cmd .= "--dport $dport "; }
			if( $state ne '' ) { $cmd .= "-m state --state $state "; }
			
			if( $is_masquerade ) {
				$cmd .= "-j MASQUERADE";
			} else {
				# Don't masquerade and return to parent chain
				$cmd .= "-j RETURN";
			}
			
			#print "$cmd\n";
			$rules .= "$cmd\n";
		}
	}
	return $rules;
}

# Apply Redirect rule
sub applyRedirect {
	my $this = shift;
	my %redirect = @_;

	my %fw = %{$this->{fw}};
	my %fwItems = %{$this->{fwItems}};
	my %services = %{$this->{services}};

	my $rules = '';	
	
	if( $redirect{ACTIVE} eq 'NO' ) {
		return '';
	}

	# Redirect or don't redirect?
	my $is_redirect = $redirect{REDIRECT} ne 'NO';

	my $src = $redirect{SRC};
	my $dst = $redirect{DST};

	# Vedo se come sorgente ho un group
	if( $fwItems{$src} eq 'GROUP' ) {
		my %newredirect = %redirect;
		foreach my $item ( @{$fw{GROUP}{$src}{ITEMS}} ) {
			if( $item ne 'FIREWALL' ) {
				$newredirect{SRC} = $item;
				$rules .= $this->applyRedirect( %newredirect );
			}
		}
		return $rules;
	}

	# Vedo se come destinazione ho un group
	if( $fwItems{$dst} eq 'GROUP' ) {
		my %newredirect = %redirect;
		foreach my $item ( @{$fw{GROUP}{$dst}{ITEMS}} ) {
			# Ignore ZONE items (PREROUTING don't accept -o option)
			if( $item ne 'FIREWALL' && $fw{ZONE}{$item}{IF} eq '' ) {
				$newredirect{DST} = $item;
				$rules .= $this->applyRedirect( %newredirect );
			}
		}
		return $rules;
	}

	# Definisco il SERVICE
	my $service = $redirect{SERVICE};
	my $port = $redirect{PORT};
	my $toport = $redirect{TOPORT};

	my ($src_zone, $src_peer, $src_mac) = $this->expand_item( $src );
	my %src_zone_attr = $this->GetZone( $src_zone );
	my $src_if = $src_zone_attr{IF};

	my $dst_zone;
	my $dst_peer;
	my $dst_if;
	if( $dst eq '*' ) {
		$dst_zone = '*';
		$dst_peer = '0.0.0.0/0';
		$dst_if = '';
	} else {
		($dst_zone, $dst_peer) = $this->expand_item( $dst );
		my %dst_zone_attr = $this->GetZone( $dst_zone );
		$dst_if = $dst_zone_attr{IF};
	}

	print $is_redirect ? '' : 'NOT ',"REDIRECT ( service $service";
	if( $service eq 'tcp' || $service eq 'udp' ) { print "($port)"; }
	print " $src";
	if( $src_mac ne '' ) { print "(mac:$src_mac)"; }
	print " --> $dst )";
	if( $is_redirect ) {
		 print " TO LOCAL PORT $toport";
	}
	print "\n";

	# Creo le 2 catene di andata e ritorno.
	$rules .= $this->applyServiceRedirect( \%services, $service, $src_if, $src_peer, $src_mac, $dst_if, $dst_peer, $port, $toport, $is_redirect);
	
	return $rules;
}

sub applyServiceRedirect {
	my $this = shift;
	my %calledServices = ();
	return $this->_applyServiceRedirect( \%calledServices, @_ );
}

sub _applyServiceRedirect {
	my $this = shift;
	my ($ref_calledServices, $ref_services, $serviceName, $src_if, $src_peer, $src_mac, $dst_if, $dst_peer, $port, $toport, $is_redirect) = @_;

	my $rules = '';
	
	my %service = %{$ref_services->{$serviceName}};

	$ref_calledServices->{$serviceName} = 1;

	# ciclo sulle regole di filering
	for( my $i = 0; $i <= $#{$service{FILTERS}}; $i++ ) {

		my %filter = %{$service{FILTERS}[$i]};

		if( $filter{SERVICE} ne '' && !$ref_calledServices->{$filter{SERVICE}} ) {
			# It is a subservice, recursion call to _applyService
			$rules .= $this->_applyServiceRedirect( $ref_calledServices, $ref_services, $filter{SERVICE},
				$src_if, $src_peer, $src_mac, $dst_if, $dst_peer, $port, $toport, $is_redirect );
			next;
		}

		my $direction = $filter{DIRECTION};
		my $p = $filter{P};
		my $icmptype = $filter{ICMPTYPE};
		my $sport = $filter{SPORT};
		my $dport = $filter{DPORT};
		my $state = $filter{STATE};
		my $jump = $filter{JUMP};

		# I only use the first tcp/udp filter rule
		if( $direction eq 'go' && ($p eq 'tcp' || $p eq 'udp' || $p eq '') &&
		    ($filter{JUMP} eq '' || $filter{JUMP} eq 'ACCEPT') ) {

			if( $dport eq 'PORT' ) {
				$dport = $port;
			}

			my $cmd = "-A REDIR ";
			if( $src_if ne '' ) { $cmd .= "-i $src_if "; }
			if( $src_peer ne '0.0.0.0/0' ) { $cmd .= "-s $src_peer "; }
			if( $src_mac =~ /^[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}$/ ) {
				$cmd .= "-m mac --source-mac $src_mac ";
			}

			# iptables prerouting chain don't accept -o option.
			#if( $dst_if ne '' ) { $cmd .= "-o $dst_if "; }
			if( $dst_peer ne '0.0.0.0/0' ) { $cmd .= "-d $dst_peer "; }

			if( $p ne '' ) {
				$cmd .= "-p $p ";
			} else {
				$cmd .= "-p * ";
			}

			#if( $icmptype ne '' ) { $cmd .= "--icmp-type $icmptype "; }
			if( $sport ne '' ) { $cmd .= "--sport $sport "; }
			if( $dport ne '' ) { $cmd .= "--dport $dport "; }
			if( $state ne '' ) { $cmd .= "-m state --state $state "; }

			if( $is_redirect ) {
				if( $toport eq '' ) {
					$cmd .= "-j REDIRECT";
				} else {
					$cmd .= "-j REDIRECT --to-port $toport";
				}
			} else {
				# Don't redirect and return to parent chain
				$cmd .= "-j RETURN";
			}

			if( $p ne '' ) {
				$rules .= "$cmd\n";
			} else {
				# I must explode '-p *' in -p tcp e -p udp
				$cmd =~ s/ \-p \*/ -p tcp/;
				$rules .= "$cmd\n";
				$cmd =~ s/ \-p tcp/ -p udp/;
				$rules .= "$cmd\n";
			}
		}
	}
	return $rules;
}

# Applica una regola di filtro del firewall
sub applyRule {
	my $this = shift;
	my $display = shift;
	my $mangle = shift;
	my %rule = @_;

	if( $rule{ACTIVE} eq 'NO' ) {
		return '';
	}
	
	my %fw = %{$this->{fw}};
	my %fwItems = %{$this->{fwItems}};
	my %services = %{$this->{services}};

	my $rules = '';
	
	my $src = $rule{SRC};
	my $dst = $rule{DST};
	my $target = $rule{TARGET};
	my $service = $rule{SERVICE};
	my $port = $rule{PORT};
	my $mark = $rule{MARK};

	if( $display ) {
		if( $target=~ /DROP|REJECT/ ) {
			print "$target $service";
		} else {
			print "ALLOW $service";
		}
		if( $service eq 'tcp' || $service eq 'udp' ) { print "($port)"; }
		print " $src";
		#if( $src_mac ne '' ) { print "(mac:$src_mac)"; }
		print " --> $dst\n";
	}

	my @srcs = ();
	my @src_list = split( /,/, $src );
	foreach my $s (@src_list) {
		if( $s eq '*' ) {
			# all zones
			foreach my $item ( sort(keys(%{$fw{ZONE}})) ) {
				if( $item ne 'FIREWALL' ) {
					push @srcs, $item;
				}
			}
		} elsif( $fwItems{$s} eq 'GROUP' ) {
			# source is a group
			foreach my $item ( @{$fw{GROUP}{$s}{ITEMS}} ) {
				push @srcs, $item;
			}
		} else {
			push @srcs, $s;
		}
	}
	# sort
	@srcs = sort(@srcs);
	# unique values
	my $prev = '***none***';
	@srcs = grep($_ ne $prev && (($prev) = $_), @srcs);
	if( $#srcs > 0 ) {
		# more then one element
		my %newrule = %rule;
		foreach my $s (@srcs) {
			$newrule{SRC} = $s;
			$rules .= $this->applyRule( 0, $mangle, %newrule );
		}
		return $rules;
	} else {
		$src = shift @srcs;
	}

	my @dsts = ();
	my @dst_list = split( /,/, $dst );
	foreach my $d (@dst_list) {
		if( $d eq '*' ) {
			# all zones
			foreach my $item ( sort(keys(%{$fw{ZONE}})) ) {
				if( $item ne 'FIREWALL' ) {
					push @dsts, $item;
				}
			}
		} elsif( $fwItems{$d} eq 'GROUP' ) {
			# source is a group
			foreach my $item ( @{$fw{GROUP}{$d}{ITEMS}} ) {
				push @dsts, $item;
			}
		} else {
			push @dsts, $d;
		}
	}
	# sort
	@dsts = sort(@dsts);
	# unique values
	my $prev = '***none***';
	@dsts = grep($_ ne $prev && (($prev) = $_), @dsts);
	if( $#dsts > 0 ) {
		# more then one element
		my %newrule = %rule;
		foreach my $d (@dsts) {
			$newrule{DST} = $d;
			$rules .= $this->applyRule( 0, $mangle, %newrule );
		}
		return $rules;
	} else {
		$dst = shift @dsts;
	}

	# service is a list of services?
	if( $service =~ /,/ ) {
		my @services = split( /,/, $service );
		my %newrule = %rule;
		foreach my $serv (@services) {
			$newrule{SERVICE} = $serv;
			$rules .= $this->applyRule( 0, $mangle, %newrule );
		}
		return $rules;
	}

	my ($src_zone, $src_peer, $src_mac) = $this->expand_item( $src );
	my ($dst_zone, $dst_peer) = $this->expand_item( $dst );

	if( $src_zone eq 'FIREWALL' && $dst_zone eq 'FIREWALL' ) {
		# ignore chain FIREWALL-FIREWALL
		if( !$mangle ) {
			print "** FIREWALL-->FIREWALL ignored **\n";
		}
		return $rules;
	}

	#command( "" );
	#comment( "# service $service: $src --> $dst  ($src_peer -> $dst_peer) [$src_zone -> $dst_zone]" );

	# Creo le 2 catene di andata e ritorno.
	my $andata = "$src_zone-$dst_zone";
	my $ritorno = "$dst_zone-$src_zone";
	
	if( $mangle ) {
		if( $mark ne '' ) {
			$rules .= $this->applyService( \%services, $service, $andata, $ritorno, $src_peer, $src_mac, $dst_peer, $port, $target, $mark );
		}
	} else {
		$rules .= $this->applyService( \%services, $service, $andata, $ritorno, $src_peer, $src_mac, $dst_peer, $port, $target, '' );
	}
	
	return $rules;
}

sub applyService {
	my $this = shift;
	my %calledServices = ();
	return $this->_applyService( \%calledServices, @_ );
}

# Applica un servizio
sub _applyService {
	my $this = shift;
	my( $ref_calledServices, $ref_services, $serviceName, $goChain, $backChain, $src, $src_mac, $dst, $port, $target, $mangle_mark ) = @_;

	my %service = %{$ref_services->{$serviceName}};

	my $rules = '';
	
	$ref_calledServices->{$serviceName} = 1;

	# commento del servizio
	#comment( "# $serviceName: ".$service{DESCRIPTION} );

	# ciclo sulle regole di filering
	my $i;
	for( $i = 0; $i <= $#{$service{FILTERS}}; $i++ ) {

		my %filter = %{$service{FILTERS}[$i]};
	
		if( $filter{SERVICE} ne '' && !$ref_calledServices->{$filter{SERVICE}} ) {
			# It is a subservice, recursion call to _applyService
			$rules .= $this->_applyService( $ref_calledServices, $ref_services, $filter{SERVICE},
				$goChain, $backChain,$src, $src_mac, $dst, $port, $target, $mangle_mark );
			next;
		}

		my $direction = $filter{DIRECTION};
		my $p = $filter{P};
		my $icmptype = $filter{ICMPTYPE};
		my $sport = $filter{SPORT};
		my $dport = $filter{DPORT};
		my $state = $filter{STATE};
		my $jump = $filter{JUMP};

		if( $target =~ /DROP|REJECT/ && $direction ne 'go' ) {
			# Don't process Back filters
			next;
		}

		# porta impostata dalla regola del firewall
		if( $sport eq 'PORT' ) {
			$sport = $port;
		}
		if( $dport eq 'PORT' ) {
			$dport = $port;
		}

		my $cmd;
		if( $direction eq 'go' ) {
			$cmd = "-A $goChain ";
			if( $src ne '0.0.0.0/0' ) { $cmd .= "-s $src "; }
			# MAC address
			if( $src_mac =~ /^[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}$/ ) {
				$cmd .= "-m mac --mac-source $src_mac ";
			}
			if( $dst ne '0.0.0.0/0' ) { $cmd .= "-d $dst "; }
		} else {
			$cmd = "-A $backChain ";
			if( $dst ne '0.0.0.0/0' ) { $cmd .= "-s $dst "; }
			if( $src ne '0.0.0.0/0' ) { $cmd .= "-d $src "; }
		}

		if( $p ne '' ) { $cmd .= "-p $p "; }
		if( $icmptype ne '' ) { $cmd .= "--icmp-type $icmptype "; }
		if( $sport ne '' ) { $cmd .= "--sport $sport "; }
		if( $dport ne '' ) { $cmd .= "--dport $dport "; }
		if( $state ne '' ) { $cmd .= "-m state --state $state "; }

		# If target=DROP|REJECT then LOG before block
		if( $target =~ /DROP|REJECT/ ) {
			my $cmdlog = $cmd;
			my $logprefix = "TFW $goChain(".substr($target,0,3).")";
			if( length($logprefix) > 28 ) {
				# iptables need log-prefix strings up to 29 chars length
				$logprefix = substr( $logprefix, 0, 28 );
			}
			$cmdlog .= "-m limit --limit $this->{log_limit}/hour --limit-burst $this->{log_limit_burst} -j LOG --log-prefix \"$logprefix:\"";
			$rules .= "$cmdlog\n";
			$jump = $target;
		}

		# Se e' in andata accetto il passaggio del pacchetto se e' in ritorno lo invio
		# alla catena BACK che si occupa di verificare che sia realmente un pacchetto di
		# una connessione gia' aperta.
		if( $mangle_mark eq '' ) {
			# filter rule
			if( $jump eq '' ) {
				$cmd .= "-j ".( $direction eq 'go' ? 'ACCEPT' : 'BACK' );
			} else {
				$cmd .= "-j $jump";
			}
		} else {
			# mangle rule
			if( $jump eq '' ) {
				if( $direction ne 'go' && $state eq '' ) {
					# BACK
					$cmd .= "-m state --state ESTABLISHED,RELATED ";
				} 
				$cmd .= "-j MARK --set-mark $mangle_mark";
			} else {
				if( $jump eq 'ICMP-ACC' ) {
					# ICMP-ACC
					my $prot = $p eq 'icmp' ? '' : '-p icmp'; 
					$cmd = "$cmd $prot --icmp-type destination-unreachable -j MARK --set-mark $mangle_mark\n".
						"$cmd $prot --icmp-type source-quench -j MARK --set-mark $mangle_mark\n".
						"$cmd $prot --icmp-type time-exceeded -j MARK --set-mark $mangle_mark\n".
						"$cmd $prot --icmp-type parameter-problem -j MARK --set-mark $mangle_mark";
				} else {
					$cmd .= "-j MARK --set-mark $mangle_mark";
				}
			}
		}
		
		#print "\n$cmd\n";

		$rules .= "$cmd\n";
	}
	return $rules;
}

# dato il nome dell'item ritorna la zona e l'ip + netmask
sub expand_item {
	my $this = shift;
	my $item = shift;
	
	my %fw = %{$this->{fw}};
	my %fwItems = %{$this->{fwItems}};
	my $itemType = $fwItems{$item};

	my $zone = '';
	my $ip = '';
	my $mac = '';

	if( $itemType eq 'ZONE' ) {
		$zone = $item;
		$ip = '0.0.0.0/0';
	}
	if( $itemType eq 'NET' ) {
		$zone = $fw{NET}{$item}{ZONE};
		$ip = $fw{NET}{$item}{IP}.'/'.$fw{NET}{$item}{NETMASK};
	}
	if( $itemType eq 'HOST' ) {
		$zone = $fw{HOST}{$item}{ZONE};
		$ip = $fw{HOST}{$item}{IP}.'/32';
		$mac = $fw{HOST}{$item}{MAC};
	}
	return ($zone, $ip, $mac);
}

sub command {
	my $this = shift;
	my $cmd = shift;
	my $stdout = shift;

	my $out = defined($stdout) ? qx/{ $cmd; } 2>&1 1>$stdout/ : qx/{ $cmd; } 2>&1/;
	if( $out ne '' ) {
		print defined($stdout) ? "$cmd > $stdout\n$out" : "$cmd\n$out";
	}
}

sub iptables_restore_emu {
	my $this = shift;
	my $rules = shift;
	
	my $table = '';
	my @lines = split(/\n/, $rules);
	foreach my $line (@lines) {
		$line =~ s/\#(.*)$//;
		if( !$line || $line eq 'COMMIT' ) {
			next;
		}
		if( $line =~ /^\*(.*?)$/ ) {
			$table = $1 eq 'filter' ? '' : $1;
			next;
		}
		my $cmd = '';
		my $chain = '';
		my $policy = '';
		if( $line =~ /^\:(.*?) (.*?) (.*?)$/ ) {
			$chain = $1;
			$policy = $2;
			if( $chain =~ /^(INPUT|OUTPUT|FORWARD)$/ ) {
				next;
			}
			$cmd = "-N $chain". ($policy ne '-' ? " -P $policy" : ''); 
		} else {
			$cmd = $line;
		}
		if( $table ) { $cmd = "-t $table $cmd"; }
		
		$this->command("iptables $cmd");
	}
}

1;