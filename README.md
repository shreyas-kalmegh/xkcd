# XKCD Cli App

A cli application for xkcd API.

## Description

This project allows us to pull comics from the xkcd API and save it in a database. Saved comics are available through cli.

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
python task_one.py -n 21
```
* To get the image link to one of the saved comic
by its title, use this command.
```
python task_one.py -t kepler
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
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)