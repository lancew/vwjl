# Migration Notes

This is where I am keeping my notes on how I migrated the old code to new.
This will make the basis of the my German Perl Workshop 2021 talk.



1. Get the old code working.
Starting December 24th 2020; picking from last commit in March 2017.


a. Dependencies via Carton.
Plack, Plack::App::CGIBin, CGI::Emulate::PSGI, CGI::Compile, DBI, Moo, namespace::clean.
DBD::AnyData

> carton install
> carton exec  plackup -R ./ -MPlack::App::CGIBin -e 'Plack::App::CGIBin->new(root => "./")->to_app'

At this point the code "worked" in so much that it worked a little; but not fully. Compiled and ran; but did not create all the data etc.


