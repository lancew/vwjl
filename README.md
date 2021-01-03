# Virtual World Judo League (VWJL).

![screenshot of athlete view](2020-12-31.png "Screenshot of athlete view")
![screenshot of simulation view](2021-01-03.png "Screenshot of simulation view")


## Install dependencies:
 ```carton install```

## Run the app:
 ```carton exec plackup -R lib,views bin/app.psgi``` (-R lib,views for reload)

## Access the app via:
 http://localhost:5000

## Run perlcritic
 ```carton exec perlcritic -3 lib/vwjl.pm```

## Run Perltidy
 ```carton exec perltidy lib/vwjl.pm```


## Datbase

See: https://hub.docker.com/_/postgres

* ```docker pull postgres``` - To get a postgres DB docker image.
* ```docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres``` to start the instance


second attempt by following:
* https://dev.to/shree_j/how-to-install-and-run-psql-using-docker-41j2
* docker run --name postgresql-container -p 5432:5432 -e POSTGRES_PASSWORD=somePassword -d postgres

## NB
 Currently there is no DB

## TODO

* [ ] Database
* [ ] the rest




