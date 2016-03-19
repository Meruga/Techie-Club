#!/usr/bin/perl

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use DBI;
use Fcntl qw(:flock);


my $cgi = new CGI;

my $driver = "mysql"; 
my $database = "s_jmeruga";
my $dsn = "DBI:$driver:database=$database";
my $userid = "s_jmeruga";
my $password = "dingdong";

my $dbh = DBI->connect($dsn, $userid, $password ) or die $DBI::errstr;


$CGI::POST_MAX = 1024 * 5000;
my $safe_filename_characters = "a-zA-Z0-9_.-";
my $upload_dir = "/home/jmeruga/public_html/upload";

my $query = new CGI;
my $filename = $query->param("photo");
my $email_address = $query->param("email");
my $fname=$query->param("fname");
my $pass=$query->param("password");
my $gender=$query->param("radio");
my @interest = $query->param( "check" );
my $publicity=$query->param("publicity");


my $interestlist = "";
foreach(@interest){
$interestlist .= $_ . ",";
}


if ( !$filename )
{
print $query->header ( );
print "There was a problem uploading your photo (try a smaller file).";
exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '..*' );
$filename = $name . $extension;
$filename =~ tr/ /_/;
$filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ )
{
$filename = $1;
}
else
{
die "Filename contains invalid characters";
}

my $upload_filehandle = $query->upload("photo");

open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";
binmode UPLOADFILE;

while ( <$upload_filehandle> )
{
print UPLOADFILE;
}

close UPLOADFILE;
my $salt = "21";
my $enpass = crypt($pass,$salt);

my $sth = $dbh->prepare("INSERT INTO Login
                       (uname,pass )
                        values
                       (?,?)");
$sth->execute($email_address,$enpass) 
          or die $DBI::errstr;
$sth->finish();


print $query->header ( );
print <<END_HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
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
<body>
		<div class="container">
			<div class="menu-wrap">
				<nav class="menu">
					<div class="icon-list">
						<a href="index.html"><i class="fa fa-home"></i><span>Home</span></a>
						<a href="regis.html"><i class="fa fa-user" ></i><span>Register</span></a>
						<a href="login.html"><i class="fa fa-power-off"></i><span>Login</span></a>
						<a href="#"><i class="fa fa-phone"></i><span>Contact Us</span></a>

					</div>
				</nav>
			</div>
			<button class="menu-button" id="open-button"></button>
				<div align="center"  class="content-wrap">

			<br><br><br><br>
			<h1>Review your details</h1>

<br>
<p>Your email address : $email_address</p><br>
<p>Your Full Name : $fname</p><br>
<p>Your Gender : $gender</p><br>
<p>Your are interested in : $interestlist</p><br>
<p>This made you register here : $publicity</p><br>
<p>Your photo :</p><br>
<img src="http://cs99.bradley.edu/~jmeruga/upload/$filename" alt="Mountain View" style="width:304px;height:228px;" />
<br>
<br>
<br>

<button type="button" onclick="window.location.href='/~jmeruga/login.html'">Now Login </button>

<br>
<br>
<br>
<br>
<br>
<br>

				</div><!-- /content-wrap -->
		</div><!-- /container -->
		<script src="/~jmeruga/js/classie.js"></script>
		<script src="/~jmeruga/js/main.js"></script>

</body>
</html>
END_HTML