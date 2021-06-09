# XKCD Cli App

A cli application for xkcd API.

## Description

This project allows us to pull comics from the xkcd API and save it in a database. Saved comics are available through cli. Comics are pulled randomly with number id between 1 and 87.

## Getting Started

### Dependencies

* Python: 3.9.x
* MySQL: 8.x
* Python dependencies in requirements.txt
* Podman: ~> 2.2.1 or equivalent Docker version
* Podman-Compose: ~> 0.1.7dev or equivalent  Docker-Compose version

<br />

### SQL Schema
#### Schema
| Fields | Type | 
| :---: | :---: | 
| num | int | 
| name | varchar(200) | 
| alt_text | varchar(500) NULL| 
| link | varchar(500) NULL| 
| image | mediumblob NULL|
| im_link | varchar(500) NULL|

#### Indexes
| Type | Fields | 
| :---: | :---: | 
| PRIMARY | num, name | 
| UNIQUE | link | 
| UNIQUE | im_link| 

<br />

### Installing

* Clone the repository on your system.
* CD into the directory.
* Build the images using this command:
```
podman-compose -f docker-compose.yaml build --no-cache
```
<br />


### Executing program

* Run the images using this command:
```
podman-compose -f docker-compose.yaml up
```
* Start an interactive shell attaching to the python container using this command.
```
podman exec -it cli_app /bin/bash
```
* To pull the commics data and pushing it to MySQL database.
```
python app.py
```
* To get the saved comics data and printing them.
```
python task_one.py -l
``` 
* To get the image link to one of the saved comic by number id, use this command:
```
python task_one.py -n <number_id>
```
* To get the image link to one of the saved comic
by its title, use this command.
```
python task_one.py -t <title>
```
* Stop the containers gracefully.
```
podman-compose -f docker-compose.yaml down
```

<br />

### Testing the application
* We use the same images built earlier.
* If the images are not already built, build the images using this command:
```
podman-compose -f docker-compose.yaml build --no-cache
```
* Run the images using this command:
```
podman-compose -f docker-compose.test.yaml up
```
* Start an interactive shell attaching to the python container using this command.
```
podman exec -it cli_app_test /bin/bash
```
* Run the test cases.
```
python test_runner.py
```
* Stop the containers gracefully.
```
podman-compose -f docker-compose.test.yaml down
```

<br />

### Access DB from Adminer
To access the database from Adminer. Use the following link in a browser.
http://localhost:8080/

<br />

## Help

To get help on task one.
```
python task_one.py -h
```

## Authors

Contributors names and contact info

Shreyas Kalmegh
[@ShreyasKalmegh](shreyas.kalmegh@gmail.com)

## Version History

* 0.1
    * Initial Release



## Acknowledgments

Inspiration, code snippets, etc.
* [mysqltutorial](https://www.mysqltutorial.org/)
* [fedoramagazine](https://fedoramagazine.org/manage-containers-with-podman-compose/)