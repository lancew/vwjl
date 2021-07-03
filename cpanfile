requires "Dancer2" => '== 0.301004';

requires "Dancer2::Plugin::Auth::Tiny"   => '== 0.008';
requires 'Dancer2::Plugin::DBIC'         => '== 0.0100';
requires "Dancer2::Plugin::Passphrase"   => '== 3.003004';
requires "Moo"                           => '== 2.005004';
requires "DBI"                           => '== 1.643';
requires "DBD::Pg"                       => '== 3.15.0';
requires "Games::Tournament"             => '== 0.21';
requires "Games::Tournament::RoundRobin" => '== 0.02';
requires "Sort::Rank"                    => '== 0.000002';
requires "IO::Socket::SSL", '== 2.071';
requires "DateTime", '== 1.54';

recommends "YAML"             => '== 1.30';
recommends "URL::Encode::XS"  => '== 0.03';
recommends "CGI::Deurl::XS"   => '== 0.08';
recommends "HTTP::Parser::XS" => '== 0.17';

on "test" => sub {
    requires "Test::More"                => '== 1.302185';
    requires "HTTP::Request::Common"     => '== 6.33';
    requires "Perl::Tidy"                => '== 20210625';
    requires "Perl::Critic"              => '== 1.140';
    requires "Test::MockModule"          => '== v0.176.0';
    requires "Perl::Critic::Freenode"    => '== v1.0.0';
    requires "Perl::Critic::Bangs"       => '== 1.12';
    requires "Perl::Critic::TooMuchCode" => '== 0.15';
    requires "Task::Perl::Critic"        => '== 1.008';
    requires "Code::TidyAll"             => '== 0.78';
    requires "Parallel::ForkManager"     => '== 2.02';
    requires "App::UpdateCPANfile"       => '== v1.1.1';
    requires "WebService::SQLFormat"     => '== 0.000007';
};

