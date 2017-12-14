# Coder Directory Api

[![Build Status](https://travis-ci.org/seekheart/coder_directory_api.svg?branch=master)](https://travis-ci.org/seekheart/coder_directory_api)
[![license](https://img.shields.io/badge/license-MIT%20License-blue.svg)](https://img.shields.io/badge/license-MIT%20License-blue.svg)
[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)


The Coder Directory Api is a RESTful api developed to provide management of
coders and programming languages.

## Resources

| Resource | Description |
| /register | Registers a user/app to use api |
| /login | Login user to obtain token |
| /login/token | Send your tokens here to refresh your access before it expires |
| /users | Access users resource for GET/POST |
| /users/{id} | Access users resource for GET/PATCH/DELETE for 1 user |
| /languages | Access language resource for GET/POST |
| /languages/{id} | Access language resource for GET/PATCH/DELETE of 1 language |


## Development

In order to run the project on your local machine you will need the following:

- [ ] Python 3.3+
- [ ] Mongodb
- [ ] Virtualenv (optional but recommended)

Additionally there is also a dockerized version of the application if you wanted
to just run the app without installing dependencies.

## Installation

To begin if you are using virtualenv you can run:

```bash
virtualenv -p <path to python3> venv
source venv/bin/activate
```

This will spin up a virtual environment with python3 as your default python.

To install the packages and dependencies of the project run the following
at the project root:

```bash
pip install -r requirements.txt
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

In addition for `APP_ENV` this variable will determine whether the app outputs
debug messages if not in `PROD` and whether or not `MULTITHREADING` for 
concurrent calls will be allowed.

### SECRET file
Your secret file should include mongo credentials 
`[db_host, db_port, db_name]` and a `secretKey` to use for app
signatures for JWT.


## Author

* **Mike Tung** - *Main Developer* - [Github]

[Github]: https://github.com/seekheart
