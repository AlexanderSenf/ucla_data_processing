# Data Processing test program

This is a test program writtent to extract data from a given text file.

This program was written using:
* Ubuntu 18.04 LTS
* Python 3.6.9

## Setup

It is recommended to set up a virtual environment:

```console
python3 -m venv env
source env/bin/activate
```

Check out the project and change into the directory:

```console
git clone https://github.com/AlexanderSenf/ucla_data_processing.git
cd ucla_data_processing
```

Once in the environment, all necessary Python prerequisites can be installed:

```console
pip install -r requirements.txt
```

This list contains one optional requirement `python-Levenshtein`, which is used
to speed up fuzzy string matching (used in case an unknown product code is 
encountered). The Linux prerequisites for this include `gcc` and `python3-dev`.

In Ubuntu these are installed:

```console
sudo apt-get install gcc python3-dev
```

## Testing the program

Unit tests: `python -m unittest`

## Running the program

The simplest form: `python processor/process.py process`
This runs the program with the provided test data file by default.

Help is displayed:  `python processor/process.py --help`

There are two commands available in the script:
* `process` is used to process an input file.
* `add` is used to add a product code to the list of recognized codes.

### process

There are three parmeters:
* The parameter `--filename` can be used to specify alternate input files.
* The parameter `--productcode` can be used to specify a specific product code.
Specifying a code displays all subtypes for that code in the purchase.
* The parameter `--uniqueids` is a flag, which is False by default. If it is
set, all unique IDs are displayed for each product code in the purchase.

The script can automatically correct for errors in the product code, if at most
one of the characters is incorrect. 

### add

There are two parmeters, both are required:
* The parameter `--productcode` specifes the new 4-letter product code.
* The parameter `--description` specifes the product description.
