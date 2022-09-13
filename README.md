# Web Log Parser

A utility to parse gzipped web server logs into a sqlite database for analysis.


## Installation

This project requires python 3.10 and pipenv.
Download Python 3.10 from https://python.org. Once installed, run the following to install pipenv:

```bash
pip install --upgrade pip
pip install pipenv
```

Then go ahead and clone the project:

```bash
git clone https://github.com/jamie-r-davis/web-log-parser.git
```

Navigate into the project directory and install its dependencies:
```bash
cd web-log-parser
pipenv install
```


## Usage
There are two commands provided by the project:

### parse
The `parse` command will recursively find all `*.gz` files within your data directory and insert them into your database. The command takes one or more domain arguments which will allow you to specify specific domain subfolders to parse. Otherwise pass `all` to the command to recursively load all files in your data directory.

```bash
# parse all .gz files in data directory
pipenv run python main.py parse all

# parse a specific domain within the data directory
pipenv run python main.py parse engin

# parse multiple domains within the data directory
pipenv run python main.py parse admissions engin umjobs
```

### parse-glob
The `parse-glob` command will all files within the data directory that match the provided glob pattern and insert them into your database. Remember to quote your glob patterns!!

```bash
pipenv run python main.py parse-glob '*umjobs*.gz'
```