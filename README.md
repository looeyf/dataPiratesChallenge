<h1 align="center">
    Data Pirates Challenge
</h1>

<h3 align="center">
    This repository contains a solution developed to solve the Data Pirates Challenge proposed by <a href="https://www.neoway.com.br/" target="_blank">Neoway</a>.
</h3>

<h4 align="center"> 
	 Status: Finished
</h4>

<p align="center">
 <a href="#about">About</a> •
 <a href="#how-it-works">How it works</a> • 
 <a href="#tech-stack">Tech Stack</a> • 
</p>

## About

The challenge consists to search for zip codes from a [URL](http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm) located in the Brazilian post office website, separate the records by FU, set an ID for each zip code and output it as a [JSONL](http://jsonlines.org) file.

---

## How it works

This project has a python file that performs the necessary functions to complete the challenge.

### Pre-requisites

Before you begin, you will need to have the following tools installed on your machine:
[Git](https://git-scm.com/downloads), latest stable release of [Python3](https://www.python.org/downloads/) (3.9.0 to the present date).

In addition, it is good to have an editor to work with the code like [VSCode](https://code.visualstudio.com/)

#### With everything installed, the following steps, you must do

```bash

# Install the following dependencies
$ pip install requests
$ pip install beautifulsoup4

# Clone this repository
$ git clone https://github.com/looeyf/dataPiratesChallenge.git

# Access the project folder cmd/terminal
$ cd dataPiratesChallenge

# Run the .py file
$ python dataPiratesChallenge.py

```

Wait for the program to finish and open the .JSON file that will be generated at the project folder to see the results.
P.S.: JSON files can be opened with your favorite browser.

---

## Tech Stack

The following tools were used in the construction of the project:

- **[python](https://www.python.org)**
- **[requests](https://pypi.org/project/requests/)**
- **[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)**
