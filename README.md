# Coder Directory Api

[![Build Status][travis]](https://travis-ci.org/seekheart/coder_directory_api)
[![License][license]](https://img.shields.io/badge/license-MIT%20License-blue.svg)
[![Version][version]](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)
[![Maintainability][maintain]](https://codeclimate.com/github/seekheart/coder_directory_api/maintainability)

The Coder Directory Api is a RESTful api developed to provide management of
coders and programming languages.

## Resources

| Resource | Description |
| --------- | ---------- |
| /register | Registers a user/app to use api |
| /login | Login user to obtain token |
| /login/token | Send your tokens here to refresh your access before it expires |
| /google | Sign in to google and get access token |
| /users | Access users resource for GET/POST |
| /users/{id} | Access users resource for GET/PATCH/DELETE for 1 user |
| /languages | Access language resource for GET/POST |
| /languages/{id} | Access language resource for GET/PATCH/DELETE of 1 language |


With the exception of the `register`, `google`, and `login` endpoints all resources
require a jwt to be sent in the `Authorization` header with `Bearer` scheme.

## Development

In order to run the project on your local machine you will need the following:

* Python 3.3+
* Mongodb
* Virtualenv (optional but recommended)

Additionally there is also a dockerized version of the application if you wanted
to just run the app without installing dependencies. In which case you will need
to install docker and docker-compose.

To spin up the docker containers simply run:

```bash
# you have to be in the project root folder.
$ docker-compose build
$ docker-compose up -d

# You can now curl the app at localhost:6000/<base url or dev by default>
# To close run the following.
$ docker-compose down
```

## Installation

To begin if you are using virtualenv you can run:

```bash
$ virtualenv -p <path to python3> venv
$ source venv/bin/activate
```
T
This will spin up a virtual environment with python3 as your default python.

To install the packages and dependencies of the project run the following
at the project root:

```bash
$ pip install -r requirements.txt
```

## Running the app

Before you can run the app a few environment variables need to be set.
These variables are needed in order to set db and api credentials as well as app
specific settings.

The following variables need to be set.

* APP_ENV - mode in which the app should be run, defaults to dev
* HOST - host address to run app on, defaults to localhost or 0.0.0.0
* PORT - port number to run on, defaults to 3000
* SECRET - path to your secret credentials json file.
* GOOGLE - path to your google credentials json file.

In addition for `APP_ENV` this variable will determine whether the app outputs
debug messages if not in `PROD` and whether or not `MULTITHREADING` for 
concurrent calls will be allowed.

### SECRET file
Your secret file should include mongo credentials 
`[db_host, db_port, db_name]` and a `secretKey` to use for app
signatures for JWT. 
Included in the project is an example setup file: `dev_settings.json`


### GOOGLE credentials
In order to use google oauth you will need to register a service account with
[google].

## Author

* **Mike Tung** - *Main Developer* - [Github]

[Github]: https://github.com/seekheart
[travis]: https://travis-ci.org/seekheart/coder_directory_api.svg?branch=master
[license]: https://img.shields.io/badge/license-MIT%20License-blue.svg
[version]: https://img.shields.io/badge/Version-1.1.0-brightgreen.svg
[google]: https://console.developers.google.com
[maintain]: https://api.codeclimate.com/v1/badges/47c92b40567f27394cec/maintainability
