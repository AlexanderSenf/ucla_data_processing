# Data Processing test program

This is a test program writtent to extract data from a given text file (Question 1).

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

The simplest form: `python processor/process.py`
This runs the program with the provided test data file by default.

Help is displayed:  `python processor/process.py --help`

The parameter `--filename` can be used to specify alternate input files.
