requires "Dancer2" => "0.300005";

requires "Dancer2::Plugin::Auth::Tiny" => "0.008";
requires 'Dancer2::Plugin::DBIC'       => "0.0100";
requires "Dancer2::Plugin::Passphrase" => "3.3.4";
requires "Moo"                         => "2.004004";
requires "DBI";
requires "DBD::Pg" => "3.14.2";
requires "Games::Tournament";
requires "Games::Tournament::RoundRobin";
requires "Sort::Rank";
requires "IO::Socket::SSL";
requires "DateTime";

recommends "YAML"             => "0";
recommends "URL::Encode::XS"  => "0";
recommends "CGI::Deurl::XS"   => "0";
recommends "HTTP::Parser::XS" => "0";

on "test" => sub {
    requires "Test::More"                => "0";
    requires "HTTP::Request::Common"     => "0";
    requires "Perl::Tidy"                => "0";
    requires "Perl::Critic"              => "0";
    requires "Test::MockModule"          => "0";
    requires "Perl::Critic::Freenode"    => "0";
    requires "Perl::Critic::Bangs"       => "0";
    requires "Perl::Critic::TooMuchCode" => "0";
    requires "Task::Perl::Critic"        => "0";
    requires "Code::TidyAll"             => "0";
    requires "Parallel::ForkManager"     => "0";
};
