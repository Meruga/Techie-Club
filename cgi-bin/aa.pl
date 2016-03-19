#!/usr/bin/perl -wT
use strict; 
use CGI; 
use Fcntl qw(:flock);

print "Content-type: text/html\n\n";
my $username="swaroop";
my $password = "password"; 
my $logincheck = "fail";
		
my $salt = "21";
my $enpass = crypt($password,$salt);
open(PASSWDDATA, "<passwd.txt") or die "Can not open users.txt";

break: while(<PASSWDDATA>)
{
	my $line = $_;
	my @namepass = split(' ',$line);
	if($namepass[0] eq $username && $namepass[1] eq $enpass)
	{
	  $logincheck = "success";


	  last break;
	}
		  
}
close(PASSWDDATA);


print $logincheck;