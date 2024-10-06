requires "Dancer2" => '== v1.1.1';

requires "Dancer2::Plugin::Auth::Tiny"   => '== 0.008';
requires 'Dancer2::Plugin::DBIC'         => '== 0.0100';
requires "Dancer2::Plugin::Passphrase"   => '== 3.004001';
requires "Moo"                           => '== 2.005005';
requires "DBI"                           => '== 1.645';
requires "DBD::Pg"                       => '== 3.18.0';
requires "Games::Tournament"             => '== 0.21';
requires "Games::Tournament::RoundRobin" => '== 0.02';
requires "Sort::Rank"                    => '== 0.000002';
requires "IO::Socket::SSL", '== 2.089';
requires "DateTime", '== 1.65';
requires "WebService::SQLFormat", '== 0.000007';
requires "JSON::MaybeXS", '== 1.004008';

recommends "YAML"             => '== 1.31';
recommends "URL::Encode::XS"  => '== 0.03';
recommends "CGI::Deurl::XS"   => '== 0.08';
recommends "HTTP::Parser::XS" => '== 0.17';

on "test" => sub {
    requires "Test::More"                => '== 1.302204';
    requires "HTTP::Request::Common"     => '== 6.46';
    requires "Perl::Tidy"                => '== 20240903';
    requires "Perl::Critic"              => '== 1.152';
    requires "Test::MockModule"          => '== v0.179.0';
    requires "Perl::Critic::Freenode"    => '== v1.0.3';
    requires "Perl::Critic::Bangs"       => '== 1.12';
    requires "Perl::Critic::TooMuchCode" => '== 0.19';
    requires "Task::Perl::Critic"        => '== 1.008';
    requires "Code::TidyAll"             => '== 0.84';
    requires "Parallel::ForkManager"     => '== 2.03';
    requires "App::UpdateCPANfile"       => '== v1.1.1';
    requires "WebService::SQLFormat"     => '== 0.000007';
};

