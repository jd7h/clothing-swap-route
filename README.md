# clothing-swap-route

## Goal
This repository aims to make the lives of the Dutch Clothing Loop managers easier by suggesting a logical route past all participating addresses of a clothing loop.
The ordering in addresses should be made in such a way that none of the participants has to walk very far, preferably < 10 minutes.

## Installation

This project is built using the programming language Python, specifically version 3. It contains a few dependencies outside of the
standard library of Python. The most easy way to install these dependencies is by using `pip` inside a Python _virtual environment_
or _venv_.

Please refer to the [documentation of `pip`](https://pip.pypa.io/en/stable/installation/) on how to install `pip` on your operating system of choice.

1. Make sure you have a recent _clone_ of this repository (e.g. `git clone https://github.com/jd7h/clothing-swap-route`)
2. Create a Python _virtual environment_. How to do this [depends on your operating system](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments)`:
    * Linux/MacOS: `python3 -m venv venv`
    * Windows: `py -m venv venv`
    * This will create a new directory called `venv` that contains your freshly created virtual environment
3. Activate the virtual environment:
    * Linux/MacOS (with `bash`): `source venv/bin/activate`
    * Windows: `venv\Scripts\activate`
4. Install the required dependencies: `pip install -r requirements.txt`
5. Done!

## Example

After installation, run the following command to get a demonstration of the capabilities of the program:

```
source venv/bin/activate
cd clothing_loop
python -m main -d -g -r -i ../example_data/tiny_example.csv -o ../example_data/tiny_result.csv
```

This tells the program to 
- turn **d**ebug mode on and print extra information about what the program is doing,
- **g**et location data from Nominatim,
- use OSRM **r**outing,
- take `../example_data/tiny_example.csv` as **i**nput, and
- write to `../example_data/tiny_result.csv` as **o**utput

## Contributions
Contributions are welcome. :)

Be sure to install the pre-commit hook so that all our files are formatted in the same way:

1. Open the virtual environment and install requirements with `pip install -r requirements`
2. Install the pre-commit with `pre-commit install`

Now the the files will be formatted at every `git commit`. 

## License
This code in this repository has a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license.
This license requires that reusers give credit to the creator(s). It allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, for noncommercial purposes only. If others modify or adapt the material, they must license the modified material under identical terms.

## External resources

The main program from this repository may use the [public OSRM service](https://routing.openstreetmap.de/about.html) by
[FOSSGIS](https://www.fossgis.de/). They offer routing services under [certain
conditions](https://www.fossgis.de/arbeitsgruppen/osm-server/nutzungsbedingungen/), to name a few (technical) ones:

- a valid HTTP User-Agent
- a maximum of one request per second
- commercial usage prohibited, unless they do not constitute an essential part of the commercial offer
- no high volume
- no bulk downloading of data

The main program in this repository respects these conditions. Consequently, the execution of the program may take a while. Please
do not change the limitations in place to keep the provider of this service happy.

Furthermore, the data provided is © [OpenStreetMap](https://www.openstreetmap.org/copyright) and their contributors under
[ODbL](https://opendatacommons.org/licenses/odbl/index.html) and [CC-BY-SA](https://creativecommons.org/licenses/by-sa/2.0/).
Please contribute to OpenStreetMap by [fixing the map](https://openstreetmap.org/fixthemap).
