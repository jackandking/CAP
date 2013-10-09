
use strict;
#use Win32::OLE qw(in with);
#use Win32::OLE::Const 'Microsoft Excel';
use Date::Manip;
        

my $g_excel_file = "responds.csv";


my @g_col_names = (
	"id",
	"Subject",
	"System Type",
	"Region",
	"Status",
	"Priority",
	"Owner",
	"Created",
	#"Responded",
	"Resolved"
	#"Root Cause"
	);

my %g_mapValues;	
my $g_cur_dir;
{
	use Cwd;  $g_cur_dir = getcwd;
	$g_cur_dir =~ s!/!\\!g;  $g_cur_dir =~ s/([^\\])$/$1\\/;
}
$g_excel_file = $g_cur_dir . $g_excel_file;
my $start_date;
my $rev_lw = 0; # resolved no during last week
my %mapIgnored; # ignore SDD & RAQ

&read_input();

#my $datafile = $ARGV[0];
my $outhtm;
my $outcsv;
#if( $datafile =~ m/([^\\]+)\.txt$/i)
{
	$outhtm = $g_cur_dir . "WeeklySummary_". $start_date . "_ALL.htm";
	$outcsv = $g_cur_dir . "WeeklySummary_". $start_date . "_ALL.csv";
}
#else { print("invalid input file: $datafile.\n"); `pause`;exit(0); }


# the html format
my $htm = "<HTML>\n<style>\n .top{background:#CCCCCC;cursor:pointer;}\n</style>\n";
$htm .= "<H1 align=center>Weekly Report for Supporting Issues (from $start_date)</H1>\n";

# quick summary
my $mls=0,my $gts=0,my $fms=0, my $sdd = 0, my $raq = 0, my $dcmls = 0, my $dms = 0;
my $new=0,my $open=0,my $resolved=0;
my $total=0;
foreach my $id(sort keys(%g_mapValues))
{
	next if(exists($mapIgnored{$id}));
	$total++;
	my $sys = $g_mapValues{$id}{"System Type"};
	if($sys =~ m/^\s*MLS\s*$/) { $mls++;}
	elsif($sys =~m/GTS/) { $gts++;}
	elsif($sys =~ m/FMS/) {$fms++;}
	elsif($sys =~ m/SDD/) { $sdd++; }
	elsif($sys =~ m/DCMLS/) { $dcmls++; }
	elsif($sys =~ m/RAQ/) { $raq++; }
	elsif($sys =~ m/DMS/) { $dms++; }
	
	my $status = $g_mapValues{$id}{"Status"};
	if($status =~ m/new/) { $new++;}
	elsif($status =~ m/open/) {$open++;}
	elsif($status =~ m/resolved/) { $resolved++;}
}

$htm .= "Summary of tickets over the last week:<br>";
$htm .= "<TABLE border=1 cellspacing=0 cellpadding=1>\n";
$htm .= "<TR bgColor=CCCCCC>";

$htm .= "<TD>Total</TD><TD>GTS</TD><TD>MLS</TD><TD>FMS</TD><TD>RAQ</TD>" .
###"<TD>DCMLS</TD><TD>SDD</TD><TD>DMS</TD><TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD><TD>New</TD><TD>Open</TD><TD>Resolved</TD><TD>Resolve last week</TD>";
"<TD>DCMLS</TD><TD>SDD</TD><TD>DMS</TD><TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD><TD>New</TD><TD>Open</TD><TD>Resolved</TD>";
$htm .= "</TR><TR>\n";
$htm .= "<TD>$total</TD>";
$htm .= "<TD>$gts</TD>";
$htm .= "<TD>$mls</TD>";
$htm .= "<TD>$fms</TD>";
$htm .= "<TD>$raq</TD>";
$htm .= "<TD>$dcmls</TD>";
$htm .= "<TD>$sdd</TD>";
$htm .= "<TD>$dms</TD>";
$htm .= "<TD>&nbsp;</TD>";
$htm .= "<TD>$new</TD>";
$htm .= "<TD>$open</TD>";
$htm .= "<TD>$resolved</TD>";
###$htm .= "<TD>$rev_lw</TD>";
$htm .= "</TR></table><br><br>\n";

# data table
$htm .= "Ticket details:";
$htm .= "<TABLE id=\"table\" border=1 cellspacing=0 cellpadding=1>\n";
$htm .= "<TR class=\"top\" bgColor=CCCCCC>";

# header
foreach my $key(@g_col_names)
{
	if($key eq "Subject") { $htm .= "<TD align=center>Subject</TD>"}
	else { $htm .="<TD>" . $key . "</TD>";}
}
$htm .= "</TR\n\n";

foreach my $id(sort keys(%g_mapValues))
{
	next if(exists($mapIgnored{$id}));
	$htm .= "\n\t<TR>\n";
	
	foreach my $key(@g_col_names)
	{
		my $val = $g_mapValues{$id}{$key};
		if($key =~ m/^id$/i)
		{
			$htm .= "<TD><a href=\"http://collectionscoresupport.ime.reuters.com/rt/Ticket/Display.html?id=$val\">$val</a></TD>";
		}
		else
		{
			$htm .= "<TD>" . $val . "</TD>";
		}
	}
	$htm .= "\n\t</TR>\n";
}

$htm .= "\n\n</TABLE>\n";
$htm .= "<BR>Link to graph showing ticket breakdown by month can be found <a href='http://portal.emea.ime.reuters.com/sites/gqs-dev-net/taps/Projects/Helpdesk/Periodic%20Reports/CCS%20ticket%20monthly%20graph.xls'>HERE</a><BR>";
$htm .= <<"SORT_SCRIPT";
<script type="text/javascript">
 
 var tableSort = function(){
  this.initialize.apply(this,arguments);
 }
 
 tableSort.prototype = {
 
  initialize : function(tableId,clickRow,startRow,endRow,classUp,classDown,selectClass){
   this.Table = document.getElementById(tableId);
   this.rows = this.Table.rows;
   this.Tags = this.rows[clickRow-1].cells;
   this.up = classUp;
   this.down = classDown;
   this.startRow = startRow;
   this.selectClass = selectClass;
   this.endRow = (endRow == 999? this.rows.length : endRow);
   this.T2Arr = this._td2Array();
   this.setShow();
  },
  
  setShow:function(){
   var defaultClass = this.Tags[0].className;
   for(var Tag ,i=0;Tag = this.Tags[i];i++){
    Tag.index = i;
    addEventListener(Tag ,'click', Bind(Tag,statu));
   }
   var _this =this;
   var turn = 0;
   function statu(){
    for(var i=0;i<_this.Tags.length;i++){
     _this.Tags[i].className = defaultClass;
    }
    if(turn==0){
     addClass(this,_this.down)
     _this.startArray(0,this.index);
     turn=1;
    }else{
     addClass(this,_this.up)
     _this.startArray(1,this.index);
     turn=0;
    }
   }
  },
  colClassSet:function(num,cla){
   for(var i= (this.startRow-1);i<(this.endRow);i++){
    for(var n=0;n<this.rows[i].cells.length;n++){
     removeClass(this.rows[i].cells[n],cla);
    }
    addClass(this.rows[i].cells[num],cla);
   }
  },
  startArray:function(aord,num){
   var afterSort = this.sortMethod(this.T2Arr,aord,num);
   this.array2Td(num,afterSort);
  },
  _td2Array:function(){  
   var arr=[];
   for(var i=(this.startRow-1),l=0;i<(this.endRow);i++,l++){
    arr[l]=[];
    for(var n=0;n<this.rows[i].cells.length;n++){
     arr[l].push(this.rows[i].cells[n].innerHTML);
    }
   }
   return arr;
  },
  array2Td:function(num,arr){
   this.colClassSet(num,this.selectClass); 
   for(var i= (this.startRow-1),l=0;i<(this.endRow);i++,l++){
    for(var n=0;n<this.Tags.length;n++){
     this.rows[i].cells[n].innerHTML = arr[l][n]; 
    }
   }
  },
  sortMethod:function(arr,aord,w){
   //var effectCol = this.getColByNum(whichCol);
   arr.sort(function(a,b){
    x = killHTML(a[w]);
    y = killHTML(b[w]);
    x = x.replace(/,/g,'');
    y = y.replace(/,/g,'');
    switch (isNaN(x)){
     case false:
     return Number(x) - Number(y);
     break;
     case true:
     return x.localeCompare(y);
     break;
    }
   });
   arr = aord==0?arr:arr.reverse();
   return arr;
  }
 }
 /*-----------------------------------*/
 function addEventListener(o,type,fn){
  if(o.attachEvent){o.attachEvent('on'+type,fn)}
  else if(o.addEventListener){o.addEventListener(type,fn,false)}
  else{o['on'+type] = fn;}
 }
 
 function hasClass(element, className) { 
  var reg = new RegExp('(\\\\s|^)'+className+'(\\\\s|\$)'); 
  return element.className.match(reg); 
 } 
  
 function addClass(element, className) { 
  if (!this.hasClass(element, className)) 
  { 
   element.className += " "+className; 
  } 
 } 
  
 function removeClass(element, className) { 
  if (hasClass(element, className)) { 
   var reg = new RegExp('(\\\\s|^)'+className+'(\\\\s|\$)'); 
   element.className = element.className.replace(reg,' '); 
  } 
 } 
 
 var Bind = function(object, fun) {
  return function() {
   return fun.apply(object, arguments);
  }
 }
 function killHTML(str){
  return str.replace(/<[^>]+>/g,"");
 }
 //------------------------------------------------
 var ex1 = new tableSort('table',1,2,999,'up','down','hov');
</script>
SORT_SCRIPT

$htm .= "\n</HTML>\n";

die("can't create file $outhtm.\n") if not open(OUT1, ">$outhtm");
print(OUT1 $htm);
close(OUT1);

# read input from excel file
sub read_input()
{
	my %mapColNameNo;
	
	my @arr = `cat $g_excel_file`;
	my $row = 0;
	foreach my $line(@arr)
	{
		if($line =~ m/#start_date: (.+)/) { $start_date = $1; }
		if($line =~ m/#resolved_lw: (.+)/) { $rev_lw = $1; }
		next if($line =~ m/^\s*#/);
		
		my @values = split(/\t/,$line);
		# header line
		if($row == 0)
		{
			for(my $i = 0; $i < scalar(@values);$i++)
			{
				my $val = @values[$i];
				$val =~ s/^CF-//;
				chomp($val);
				$mapColNameNo{$val} = $i;
			}
		}
		else # data lines
		{
			foreach my $Name(@g_col_names)
			{
				my $id = @values[0];
				if(not exists($mapColNameNo{$Name}))
				{
					if($Name ne "Responded")
					{
						print("Error: can't find $Name.\n");
					}
					next;
				}
				my $colNo = $mapColNameNo{$Name};
				my $val = @values[$colNo];
				if($Name eq "Priority" )
				{
					if($val <= 25) { $val = "low"; }
					elsif( $val <= 50) { $val = "medium";}
					else { $val = "major"; }
				}
				elsif($Name eq "System Type")
				{
					$val =~ s/GQS\://g;
					$val =~ s/Legacy\://g;
					$val =~ s/Other\://g;
					$val =~ s/Elektron\://g;
					#if($val =~ m/SDD|Legacy/i) { $mapIgnored{$id} = 1; };	# ignore SDD and Legacy
				}
				elsif($Name eq "Subject")
				{
					$val =~ s/^\s*\[[^\]]+\]\s+//;
				}
				elsif($Name eq "Resolved")
				{
					if($val =~ m/^\s*$/) { $val = "NA"; }
				}
				$g_mapValues{$id}{$Name} = $val;
			}			
		}
		
		$row++;
	}
=p
	# read respond time
	{
		my @res_time = `type $g_res_time_file`;
		die("not valid respond time file $g_res_time_file.\n") if( scalar(@res_time) < 1);
		$res_time[0] =~ m/#start_date: (.+)/;
		$start_date = $1;
		for(my $i = 1; $i < scalar(@res_time);$i++)
		{
			my @values = split(/,/,$res_time[$i]);
			$g_mapValues{$values[0]}{"Responded"} = $values[1];
		}
	}
=cut
	
=test Excel
	# get or start excel app
	my $g_excel = Win32::OLE->GetActiveObject('Excel.Application')
		|| Win32::OLE->new('Excel.Application', 'Quit');
	die("Failed to start excel application.\n") if( $g_excel == undef ) ;

	# open Excel file
	my $Book = $g_excel->Workbooks->Open($g_excel_file, 0, 1);	# Open in read-only mode
	die("Failed to open file: '$g_excel_file'.\n") if( $Book == undef ) ;

	# get all needed sheets
	my $sheet = $Book->Worksheets("Results");
	die("Failed to locate Results page.\n") if(not defined($sheet));
    my $rowEnd = $sheet->UsedRange->Rows->Count;
	my $colEnd = $sheet->UsedRange->Columns->Count;
    foreach my $colNo (1..$colEnd)
	{
		my $Col = $sheet->Cells(1, $colNo)->{'Value'};
		$Col =~ s/^CF-//;
		$mapColNameNo{$Col} = $colNo;
	}
	# get values
    foreach my $row (2..$rowEnd)
	{
		my $id = $sheet->Cells($row, 1)->{'Value'};
		foreach my $Name(@g_col_names)
		{
			if(not exists($mapColNameNo{$Name}))
			{
				print("Error: can't find $Name.\n"); next;
			}
			my $colNo = $mapColNameNo{$Name};
			my $val = $sheet->Cells($row, $colNo)->{'Value'};
			if($Name =~ m/Created|Resolved/)
			{
				print("tt:$val,");
				$val = ParseDate($val);
				print("$val\n");
			}
			$g_mapValues{$id}{$Name} = $val;
		}
	}
=cut

}