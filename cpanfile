requires "Dancer2" => "0.300004";

requires "Dancer2::Plugin::Auth::Tiny" => "0.008";
requires "Moo" => "2.004004";

recommends "YAML"             => "0";
recommends "URL::Encode::XS"  => "0";
recommends "CGI::Deurl::XS"   => "0";
recommends "HTTP::Parser::XS" => "0";

on "test" => sub {
    requires "Test::More"            => "0";
    requires "HTTP::Request::Common" => "0";
    requires "Perl::Tidy"            => "0";
};
