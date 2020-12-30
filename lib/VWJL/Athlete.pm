package VWJL::Athlete;

use VWJL::Infrastructure::Database;


sub get {
    my %args = @_;
    
    return VWJL::Infrastructure::Database::get(user => $args{'user'});
}



true;



