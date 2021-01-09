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
second attempt by following:
* https://dev.to/shree_j/how-to-install-and-run-psql-using-docker-41j2
* docker run --name postgresql-container -p 5432:5432 -e POSTGRES_PASSWORD=somePassword -d postgres

## Installation (ubuntu server)
* Perl obviously
* make (nneded for some modules): ```apt install make```
* gcc: ``apt install gcc```
* postgres libs: ```apt-get install libpq-dev```
* ssl stuff: ```apt-get install zlib1g-dev```
* more ssl: ```apt-get install libssl-dev```
* cpanm ```apt update; apt install cpanminus```
* carton ```cpanm Carton```
* clone the repo: ```git clone https://github.com/lancew/vwjl.git```
* ```cd vwjl```
* Install modules: ```carton install```


## DO Hacks while building it up

I've hacked up a script to redirect, call it on DO with:

```carton exec plackup bin/redirect.psgi --port 80```

Running with SSL on DO:

```carton exec plackup -R lib,views bin/app.psgi --enable-ssl --ssl-key-file=/etc/letsencrypt/live/www.vwjl.net/privkey.pem --ssl-cert-file=/etc/letsencrypt/live/www.vwjl.net/fullchain.pem --port 443```


## TODO

* [ ] Database
* [ ] the rest




