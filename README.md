tifa
---
[![Build Status](https://travis-ci.org/wddwycc/tifa.svg?branch=master)](https://travis-ci.org/wddwycc/tifa)
[![PyPI](https://img.shields.io/pypi/v/tifa.svg)](https://pypi.python.org/pypi/tifa)
[![license](https://img.shields.io/pypi/pyversions/tifa.svg)](https://pypi.python.org/pypi/tifa)
[![license](https://img.shields.io/pypi/l/tifa.svg)](https://pypi.python.org/pypi/tifa)

A modern flask scaffolding

![](https://storage.googleapis.com/duan/etc/A45A991C-54C7-4B6A-8906-9265CE7893E8/tifa.jpg)

## Introduction

Flask and Webpack are both brilliant tool for developers to quickly setup and develop web applications. The combination of them two could meet most modern web development requirements today.

If you want to build a traditional web server:

**Web server ( Flask ) + Webpack ( pack assets )**

If you want to separate front-end and back-end:

**API Server ( Flask ) + Front-end ( A SPA framework with webpack to pack assets )**

Or more cutting-edge solution which I prefer recently, use traditional web server and Vue.js to improve user interaction by injecting web components:

**Web server ( Flask ) + Front-end improvements ( Vue.js )  + Webpack ( pack assets )**



tifa is a scaffolding designed to create these environments for you.



## Install

```
$ pip install tifa
```

## Usage

### Generate a tifa configuration file

```
$ tifa init
```

### Initialize project through configuration

```
$ tifa gen
```

This command would read `tifa.yaml` by default. To use a specific config file:

```
$ tifa gen --config path/to/config.yaml
```

By default, tifa would remove configuration file when successfully created a project.
If you want to keep it, add a `--factory` flag

```
$ tifa gen --factory
```

## Configuration Specs

```yaml
name: <project name>
# for route `front`, empty url prefix would be given.
# other routes would have its name as route prefix.
routes:
  - front
  - api
# Use camel case for model name, tablename would automatically be transformed to underscore.
models:
  - User
  - Product
# if specified, would generate associated config files in `./conf` folder
confs:
  - supervisor
  - gunicorn
  - nginx
# webpack modes
# false: Web server ( Flask ) without webpack
# classic: Web server ( Flask ) + Webpack ( pack assets )
# separate: API Server ( Flask ) + Front-end ( Vue.js with webpack to pack assets )
# radical: Web server ( Flask ) + Front-end improvements ( Vue.js ) + Webpack ( pack assets )
webpack: classic
```

