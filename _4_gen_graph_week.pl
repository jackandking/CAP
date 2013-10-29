
use strict;
use Date::Parse;
use POSIX;

my $file_hist = "all_hist.csv";
my $file_out = "all_hist_graph.csv";

die("failed to create $file_out.\n") if not open(OUT1, ">$file_out");

=queue value
1 General

3 Service Affecting 
4 Defect Report
5 Request For Help 
=cut

my $startDate = time() - 60*60*24*365;
my $startYear = strftime("%Y", gmtime($startDate) );
print( "start date: " . gmtime($startDate) . "\n");

my %mapTickets = ();

my $baseNumCreateDefect = 0;
my $baseNumCloseDefect = 0;
my $baseNumCreateHelp = 0;
my $baseNumCloseHelp = 0;

# populate input file
# Id, Create Date, Resolved Date, Status, Queue, System Type
foreach my $line( `cat $file_hist` )
{
	next if( $line =~ m/^#/ );
	
	my @data = split(/,/, $line);
	my $id 			= $data[0];
	my $createDate 	= $data[1];
	my $resolveDate = $data[2];
	my $status 		= $data[3];
	my $queue 		= $data[4];
	my $sysType 	= $data[5];
	
	#$sysType =~ s/GQS\://g;
	$sysType =~ s/Other\://g;
	$sysType =~ s/Legacy\://g;
	#next if($sysType =~ m/SDD|Legacy/i);
	
	# the ticket is created within past 1 year
	if( str2time($createDate) > $startDate ) {
		$mapTickets{$id}{createDate} 	= $createDate;
		$mapTickets{$id}{resolveDate} 	= $resolveDate;
		$mapTickets{$id}{status}		= $status;
		$mapTickets{$id}{queue} 		= $queue;
		$mapTickets{$id}{sysType}		= $sysType;
		#some tickets are created before 1 years ago, but resolved within 1 year, should be treated as 'crossyear'
		$mapTickets{$id}{crossyear}		= 0;		
	}
	else {
		if( $queue != 5 ) # not Request For Help
		{
			$baseNumCreateDefect++;
			# the ticket is closed before the $startDate
			if( $resolveDate ne "" ) { 
				if( str2time($resolveDate) <= $startDate) {
					$baseNumCloseDefect++; 
				}
				else {
					$mapTickets{$id}{createDate} 	= $createDate;
					$mapTickets{$id}{resolveDate} 	= $resolveDate;
					$mapTickets{$id}{status}		= $status;
					$mapTickets{$id}{queue} 		= $queue;
					$mapTickets{$id}{sysType}		= $sysType;				
					$mapTickets{$id}{crossyear}		= 1;
					#print "$id\n";
				}
			}
		}
		else	# Request For Help
		{
			$baseNumCreateHelp++;
			if( $resolveDate ne "" ) {  
				if( str2time($resolveDate) <= $startDate ) {
					$baseNumCloseHelp++; 
				}
				else {
					$mapTickets{$id}{createDate} 	= $createDate;
					$mapTickets{$id}{resolveDate} 	= $resolveDate;
					$mapTickets{$id}{status}		= $status;
					$mapTickets{$id}{queue} 		= $queue;
					$mapTickets{$id}{sysType}		= $sysType;								
					$mapTickets{$id}{crossyear}		= 1;
					#print "$id\n";
				}				
			}
		}	
	}
}

# map: week number => tickets count
my (%mapCreateDefect, %mapCloseDefect);
my (%mapCreateHelp, %mapCloseHelp);

# map: week number => first day of the week, like 11-Oct
my %mapWeekName; 

# ====================================================================================
# populate all created tickets
foreach my $id (sort keys %mapTickets)
{
	my $createDate 	= $mapTickets{$id}{createDate};
	my $resolveDate = $mapTickets{$id}{resolveDate};
	my $status 		= $mapTickets{$id}{status};
	my $queue 		= $mapTickets{$id}{queue};
	my $sysType 	= $mapTickets{$id}{sysType};
	my $crossyear 	= $mapTickets{$id}{crossyear};

	my $year = strftime("%Y", gmtime(str2time($createDate)) );	# extract the year
	my $numWeek = strftime("%W", gmtime(str2time($createDate)));# extract the week num
	$numWeek += ($year - $startYear) * 100;

	################################ process of createDate first
	if( !$crossyear ) {	#make sure this ticket is not cross-year
		if( $queue != 5) { #defect fix
			if (not exists $mapCreateDefect{$numWeek}) 
			{
				$mapCreateDefect{$numWeek} = 1;
				$mapWeekName{$numWeek} = strftime("%d-%b-%y", gmtime(str2time($createDate)));
			}
			else 
			{
				$mapCreateDefect{$numWeek} ++;
			}
		}
		else { #request for help
			if (not exists $mapCreateHelp{$numWeek}) 
			{
				$mapCreateHelp{$numWeek} = 1;
				$mapWeekName{$numWeek} = strftime("%d-%b-%y", gmtime(str2time($createDate)));
			}
			else 
			{
				$mapCreateHelp{$numWeek} ++;
			}
		}
	}
	####################################################################
	
	################################ process of resolveDate
	next if ($resolveDate eq "");
	
	$year = strftime("%Y", gmtime(str2time($resolveDate)) );	# extract the year
	$numWeek = strftime("%W", gmtime(str2time($resolveDate)));		# extract the week num
	$numWeek += ($year - $startYear) * 100;
	
	if( $queue != 5) { #defect fix
		if (not exists $mapCloseDefect{$numWeek}) { $mapCloseDefect{$numWeek} = 1; }
		else { $mapCloseDefect{$numWeek} ++; }
	}
	else { #request for help
		if (not exists $mapCloseHelp{$numWeek}) { $mapCloseHelp{$numWeek} = 1; }
		else { $mapCloseHelp{$numWeek} ++; }
	}
}

# ====================================================================================
# 					print the result to file
print(OUT1 "numWeek,Date,CreateWithinDefect,CloseWithinDefect,CreateTotalDefect,CloseTotalDefect,CreateWithinHelp,CloseWithinHelp,CreateTotalHelp,CloseTotalHelp,CreateTotal,CloseTotal\n");
# 
my $lastCreateDefect 		= 0;
my $lastCloseDefect 		= 0;
my $lastCreateTotalDefect 	= $baseNumCreateDefect;
my $lastCloseTotalDefect  	= $baseNumCloseDefect;
my $lastCreateHelp 		= 0;
my $lastCloseHelp 		= 0;
my $lastCreateTotalHelp = $baseNumCreateHelp;
my $lastCloseTotalHelp  = $baseNumCloseHelp;

my $lastCreateTotal = $lastCreateTotalDefect + $lastCreateTotalHelp;
my $lastCloseTotal 	= $lastCloseTotalDefect  + $lastCloseTotalHelp;

my @arr1 = keys(%mapCreateDefect);
push(@arr1, keys(%mapCreateHelp));
my %temp;
@arr1 = grep(!$temp{$_}++,@arr1);	# remove the dups
foreach my $numWeek (sort {$a <=> $b } ( @arr1 ) )
{
	print(OUT1 "$numWeek,$mapWeekName{$numWeek},");

	# for Defect issues
	if( exists $mapCreateDefect{$numWeek} ) { $lastCreateDefect = $mapCreateDefect{$numWeek} ;}
	else { $lastCreateDefect = 0; }
	if( exists $mapCloseDefect{$numWeek}) { $lastCloseDefect = $mapCloseDefect{$numWeek}; }
	else { $lastCloseDefect = 0; }
	print(OUT1 "$lastCreateDefect,$lastCloseDefect,");	
	
	$lastCreateTotalDefect += $lastCreateDefect;
	$lastCloseTotalDefect  += $lastCloseDefect;
	print( OUT1 "$lastCreateTotalDefect,$lastCloseTotalDefect,");
	
	# for request for help
	if( exists $mapCreateHelp{$numWeek} ) { $lastCreateHelp = $mapCreateHelp{$numWeek}; }
	else { $lastCreateHelp = 0; }
	if( exists $mapCloseHelp{$numWeek}) { $lastCloseHelp = $mapCloseHelp{$numWeek}; }
	else { $lastCloseHelp = 0; }
	print(OUT1 "$lastCreateHelp,$lastCloseHelp,");
	
	$lastCreateTotalHelp += $lastCreateHelp;
	$lastCloseTotalHelp  += $lastCloseHelp;
	print( OUT1 "$lastCreateTotalHelp,$lastCloseTotalHelp,");

	$lastCreateTotal 	= $lastCreateTotalDefect + $lastCreateTotalHelp;
	$lastCloseTotal 	= $lastCloseTotalDefect  + $lastCloseTotalHelp;
	print( OUT1 "$lastCreateTotal,$lastCloseTotal");
	print (OUT1 "\n");
}

close(OUT1);


