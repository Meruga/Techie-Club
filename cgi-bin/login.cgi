#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use strict;
use CGI; 
use Fcntl qw(:flock);

print "Content-type: text/html\n\n";

my $cgi = new CGI;

my $username = $cgi->param( "uname" );
my $pass12 = $cgi->param( "password" ); 
my $logincheck = "fail";
		
my $salt = "21";
my $enpass = crypt($pass12,$salt);

my $driver = "mysql"; 
my $database = "s_jmeruga";
my $dsn = "DBI:$driver:database=$database";
my $userid = "s_jmeruga";
my $password = "dingdong";

my $dbh = DBI->connect($dsn, $userid, $password ) or die $DBI::errstr;

my $sth = $dbh->prepare("SELECT * from Login");
$sth->execute() or die $DBI::errstr;

while (my @row = $sth->fetchrow_array()) {
   my ($uname, $pass ) = @row;
if($uname eq $username && $pass eq $enpass)
	{
	  $logincheck = "success";

	}
}
$sth->finish();


if($logincheck eq "success")
{

print <<'END_HTML';

<!DOCTYPE html>
<html lang="en" class="no-js">
	<head>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge"> 
		<meta name="viewport" content="width=device-width, initial-scale=1"> 
		<title>Techie Club</title>
		<meta name="description" content="Modern effects and styles for off-canvas navigation with CSS transitions and SVG animations using Snap.svg" />
		<meta name="keywords" content="sidebar, off-canvas, menu, navigation, effect, inspiration, css transition, SVG, morphing, animation" />
		<meta name="author" content="Codrops" />
		<link rel="shortcut icon" href="../favicon.ico">
		<link rel="stylesheet" type="text/css" href="/~jmeruga/css/normalize.css" />
		<link rel="stylesheet" href="/~jmeruga/css/lay.css" title="style" media="screen"/>
		<link rel="stylesheet" type="text/css" href="/~jmeruga/css/demo.css" />
		<link rel="stylesheet" type="text/css" href="/~jmeruga/fonts/font-awesome-4.2.0/css/font-awesome.min.css" />
		<link rel="stylesheet" type="text/css" href="/~jmeruga/css/menu_topexpand.css" />
		<!--[if IE]>
  		<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
		<![endif]-->
	</head>
	<body>
		<div class="container">
			<div class="menu-wrap">
				<nav class="menu">
					<div class="icon-list">
						<a href="/~jmeruga/main.html" target="iframe"><i class="fa fa-newspaper-o "></i><span>Latest News</span></a>
						<a href="/~jmeruga/coming.html" target="iframe"><i class="fa fa-mobile" ></i><span>Gadgets</span></a>
						<a href="/~jmeruga/coming.html" target="iframe"><i class="fa fa-gamepad" ></i><span>Games</span></a>
						<a href="/~jmeruga/coming.html" target="iframe"><i class="fa fa-headphones"></i><span>Music</span></a>
						<a href="/~jmeruga/index.html"><i class="fa fa-sign-out"></i><span>Exit</span></a>

					</div>
				</nav>
			</div>
			<button class="menu-button" id="open-button"></button>
			<div class="content-wrap">
				<div  id = "main" >
				
<iframe src="/~jmeruga/main.html" id="myIframe" name="iframe"/></iframe>

				</div>
				

			</div><!-- /content-wrap -->
		</div><!-- /container -->
		<script src="/~jmeruga/js/classie.js"></script>
		<script src="/~jmeruga/js/main.js"></script>
	</body>
</html>

END_HTML
}
