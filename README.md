> # Currency Exchange #

### This project is a bank currency parser

* Data packet reference [Package](https://github.com/kravchenko89/currency_exchange "Currency Exchange")

#### Installation for launching a project `Currency Exchange`

```Ubuntu
//Ubuntu

$ python3 --version or $ python3 -V
$ sudo apt-get update
$ sudo apt-get install python3
$ sudo apt-get install -y python3-venv
```
#### Creating a folder for the project
```cd
//mkdir

$ mkdir project
$ cd project
```
#### Cloning project 
```buildoutcfg//

git clone https://github.com/kravchenko89/currency_exchange.git
        # Clone with HTTPS
OR

git clone git@github.com:kravchenko89/currency_exchange.git
        # Clone with SSH
```
#### Creation of virtual `environment` and launch
```venv
//venv
$ python3 -m venv my_env

```

#### Installing `dependency` packages

```packages
//packages

$ pip install -r requirements.txt
```
* installation of packages for this project

#### Launch and building a project in `docker`
```docker
//docker

$ docker-compose -f dc.yml up -d
```
* this command will build all containers and packages from the project to docker 

#### Do database migration

```buildoutcfg//

$ docker-compose -f dc.yml run web python src/manage.py makemigrations
$ docker-compose -f dc.yml run web python src/manage.py migrate
```

#### private bank currency loading for 4 years

```buildoutcfg//
$ docker exec -it backend python src/manage.py privat_archive

```

#### Some commands for working with containers

```buildoutcfg//
$ docker-compose -f dc.yml ps    
       # view the status of running containers
```

```buildoutcfg//
$ docker ps -a 
        # view the status of all containers
```

```buildoutcfg//
$ docker ps -a 
        # view the status of all containers
```

```buildoutcfg//

docker exec -it backend python src/manage.py shell_plus

```

```buildoutcfg//

docker logs -f [name image]
        # view logs
```