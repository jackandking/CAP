
use strict;
use Date::Parse;
use POSIX;

my $file_hist = "all_hist.csv";
my $file_out = "all_hist_graph_month.csv";

die("failed to create $file_out.\n") if not open(OUT1, ">$file_out");

=queue value
1 General

3 Service Affecting 
4 Defect Report
5 Request For Help 
=cut

#my $startDate = time() - 60*60*24*365;
my $startDate = time();
my $startYear = strftime("%Y", gmtime($startDate) );
$startYear -= 1;
my $startMonth = strftime("%m", gmtime($startDate) );
#print( "start date: " . gmtime($startDate) . "\n");

my %mapTickets = ();

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
	my $region	 	= $data[6];
	
	#$sysType =~ s/GQS\://g;
	#$sysType =~ s/Other\://g;
	#$sysType =~ s/Legacy\://g;
	#next if($sysType =~ m/SDD|Legacy/i);
	
	my $createYear 	 = strftime("%Y", localtime(str2time($createDate)) );
	my $createMonth  = strftime("%m", localtime(str2time($createDate)) );
	my $resolveYear  = strftime("%Y", localtime(str2time($resolveDate)) );
	my $resolveMonth = strftime("%m", localtime(str2time($resolveDate)) );

	my $interest = 0;
	
	# the ticket is created within past 1 year
	if( (($createYear > $startYear)) or
		(($createYear == $startYear) and ($createMonth > $startMonth)) ) {
		#some tickets are created before 1 years ago, but resolved within 1 year, should be treated as 'crossyear'
		$mapTickets{$id}{crossyear}		= 0;
		$interest = 1;
	}
	elsif( (($resolveYear > $startYear)) or
		(($resolveYear == $startYear) and ($resolveMonth > $startMonth)) ) {
		$mapTickets{$id}{crossyear}		= 1;		
		$interest = 1;
	}
	
	if( $interest ) {
		$mapTickets{$id}{createYear} 	= $createYear;
		$mapTickets{$id}{createMonth} 	= $createMonth;
		$mapTickets{$id}{resolveYear} 	= $resolveYear;
		$mapTickets{$id}{resolveMonth} 	= $resolveMonth;
		$mapTickets{$id}{createDate} 	= $createDate;
		$mapTickets{$id}{resolveDate} 	= $resolveDate;
		$mapTickets{$id}{status}		= $status;
		$mapTickets{$id}{queue} 		= $queue;
		$mapTickets{$id}{sysType}		= $sysType;	
		$mapTickets{$id}{region}		= $region;
	}
}

# map: month number => tickets count
my (%mapMonthCreate, %mapMonthClose);

# ====================================================================================
# populate all created tickets
foreach my $id (sort keys %mapTickets)
{
	my $createYear 	= $mapTickets{$id}{createYear};
	my $createMonth = $mapTickets{$id}{createMonth};
	my $resolveYear = $mapTickets{$id}{resolveYear};
	my $resolveMonth = $mapTickets{$id}{resolveMonth};
	my $createDate 	= $mapTickets{$id}{createDate};
	my $resolveDate = $mapTickets{$id}{resolveDate};
	my $status 		= $mapTickets{$id}{status};
	my $queue 		= $mapTickets{$id}{queue};
	my $sysType 	= $mapTickets{$id}{sysType};
	my $region		= $mapTickets{$id}{region};
	my $crossyear 	= $mapTickets{$id}{crossyear};

	my $numMonth = $createYear."-".$createMonth;

	################################ process of createDate first
	if( !$crossyear ) {	#make sure this ticket is not cross-year	
		$mapMonthCreate{$numMonth}{total} ++;
		
		if( $sysType =~ /GQS/) {
			$mapMonthCreate{$numMonth}{GQS} ++;
		}
		elsif( $sysType =~ /SDD/) {
			$mapMonthCreate{$numMonth}{SDD} ++;
		}
		elsif( $sysType =~ /Legacy/) {
			$mapMonthCreate{$numMonth}{Legacy} ++;
		}
		elsif( $sysType =~ /Elektron/) {
			$mapMonthCreate{$numMonth}{Elektron} ++;
		}
		else {
			#print "$id, $sysType\n";
		}
		
		if( $region =~ /APAC/) {
			$mapMonthCreate{$numMonth}{APAC} ++;
		}
		elsif( $region =~ /EMEA/) {
			$mapMonthCreate{$numMonth}{EMEA} ++;
		}
		elsif( $region =~ /AMERS/) {
			$mapMonthCreate{$numMonth}{AMERS} ++;
		}
	}
		
	################################ process of resolveDate
	next if ($resolveDate eq "");
	
	$numMonth = $resolveYear."-".$resolveMonth;
	
	$mapMonthClose{$numMonth}{total} ++; 
	
	if( $sysType =~ /GQS/) {
		$mapMonthClose{$numMonth}{GQS} ++;
	}
	elsif( $sysType =~ /SDD/) {
		$mapMonthClose{$numMonth}{SDD} ++;
	}
	elsif( $sysType =~ /Legacy/) {
		$mapMonthClose{$numMonth}{Legacy} ++;
	}
	elsif( $sysType =~ /Elektron/) {
		$mapMonthClose{$numMonth}{Elektron} ++;
	}	
	else {
		#print "$id, $sysType\n";
	}	
	
	if( $region =~ /APAC/) {
		$mapMonthClose{$numMonth}{APAC} ++;
	}
	elsif( $region =~ /EMEA/) {
		$mapMonthClose{$numMonth}{EMEA} ++;
	}
	elsif( $region =~ /AMERS/) {
		$mapMonthClose{$numMonth}{AMERS} ++;
	}	
}

# ====================================================================================
# 					print the result to file
print(OUT1 "Month,CreateTotal,CloseTotal,CreateGQS,CloseGQS,CreateLegacy,CloseLegacy,CreateSDD,CloseSDD,CreateElektron,CloseElektron,CreateEMEA,CloseEMEA,CreateAMERS,CloseAMERS,CreateAPAC,CloseAPAC\n");

print(OUT1    "Month,Total,Total,GQS,GQS,RAQ/DCMLS/TQS,RAQ/DCMLS/TQS,SDD,SDD,CVA/CVG,CVA/CVG,EMEA,EMEA,AMERS,AMERS,APAC,APAC\n");

my @arr1 = keys(%mapMonthCreate);
push(@arr1, keys(%mapMonthClose));
my %temp;
@arr1 = grep(!$temp{$_}++,@arr1);	# remove the dups
my @arr2 = sort @arr1;
foreach my $numMonth ( @arr2 )
{
	print(OUT1 "$numMonth,");
	my $numCreate = 0;
	my $numClose  = 0;
	if( exists $mapMonthCreate{$numMonth} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{total};
	}
	if( exists $mapMonthClose{$numMonth} ) { 
		$numClose = $mapMonthClose{$numMonth}{total};
	}
	print(OUT1 "$numCreate,$numClose,");
	
	#GQS
	$numCreate = 0;
	$numClose  = 0;
	if( exists $mapMonthCreate{$numMonth}{GQS} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{GQS};
	}
	if( exists $mapMonthClose{$numMonth}{GQS} ) { 
		$numClose = $mapMonthClose{$numMonth}{GQS};
	}	
	print(OUT1 "$numCreate,$numClose,");
	
	#Legacy
	$numCreate = 0;
	$numClose  = 0;
	if( exists $mapMonthCreate{$numMonth}{Legacy} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{Legacy};
	}
	if( exists $mapMonthClose{$numMonth}{Legacy} ) { 
		$numClose = $mapMonthClose{$numMonth}{Legacy};
	}	
	print(OUT1 "$numCreate,$numClose,");	
	
	#SDD
	$numCreate = 0;
	$numClose  = 0;
	if( exists $mapMonthCreate{$numMonth}{SDD} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{SDD};
	}
	if( exists $mapMonthClose{$numMonth}{SDD} ) { 
		$numClose = $mapMonthClose{$numMonth}{SDD};
	}	
	print(OUT1 "$numCreate,$numClose,");	
	
	#Elektron
	$numCreate = 0;
	$numClose  = 0;
	if( exists $mapMonthCreate{$numMonth}{Elektron} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{Elektron};
	}
	if( exists $mapMonthClose{$numMonth}{Elektron} ) { 
		$numClose = $mapMonthClose{$numMonth}{Elektron};
	}	
	print(OUT1 "$numCreate,$numClose,");
	
	#EMEA
	$numCreate = 0;
	$numClose  = 0;
	if( exists $mapMonthCreate{$numMonth}{EMEA} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{EMEA};
	}
	if( exists $mapMonthClose{$numMonth}{EMEA} ) { 
		$numClose = $mapMonthClose{$numMonth}{EMEA};
	}	
	print(OUT1 "$numCreate,$numClose,");	

	#AMERS
	$numCreate = 0;
	$numClose  = 0;
	if( exists $mapMonthCreate{$numMonth}{AMERS} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{AMERS};
	}
	if( exists $mapMonthClose{$numMonth}{AMERS} ) { 
		$numClose = $mapMonthClose{$numMonth}{AMERS};
	}	
	print(OUT1 "$numCreate,$numClose,");
	
	#APAC
	$numCreate = 0;
	$numClose  = 0;
	if( exists $mapMonthCreate{$numMonth}{APAC} ) { 
		$numCreate = $mapMonthCreate{$numMonth}{APAC};
	}
	if( exists $mapMonthClose{$numMonth}{APAC} ) { 
		$numClose = $mapMonthClose{$numMonth}{APAC};
	}	
	print(OUT1 "$numCreate,$numClose,");		
	
	print (OUT1 "\n");
}

close(OUT1);


