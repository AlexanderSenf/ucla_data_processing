# Data Processing test program

This is a test program writtent to extract data from a given text file (Question 2).

This program was written using:
* Ubuntu 18.04 LTS
* Python 3.6.9

## Setup

It is recommended to set up a virtual environemnt:

```console
python3 -m venv env
sourve env/bin/activate
```

Check out the project and change into the directory:

```console
git clone https://github.com/AlexanderSenf/ucla_data_processing.git
cd ucla_data_processing
```

Once in the environment, all necessary prerequisites can be installed:

```console
pip install -r requirements.txt
```

## Testing the program

Unit tests: `python -m unittest`

## Running the program

The simplest form: `python processor/process.py process`
This runs the program with the provided test data file by default.

Help is displayed:  `python processor/process.py --help`

There are two commands available in teh script:
* `process` is used to process an inpot file.
* `add` is used to add a procuct code to the list of recognized codes.

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
