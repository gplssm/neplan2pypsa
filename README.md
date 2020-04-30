# neplan2pypsa

Convert NEPLAN grid data (.edt and .ndt) to [eDisGo](https://edisgo.readthedocs.io/en/dev/)-flavored 
[PyPSA](http://www.pypsa.org/doc/index.html) format.

## Installation

You can install it locally for developing with

    python setup.py install
    
## Usage

The package provides a python function and a CLI.

### Using Python

The following code saves converted NEPLAN files as CSV in `'path/for/csv/files/'`.

```
from neplan2pypsa import neplan2pypsa

neplan2pypsa(
    'elements.edt',
    'nodes.ndt',
    'path/for/csv/files/'
    )
```

### Command-line interface

By installing _neplan2pypsa_ with pip, the command-line script `neplan2pypsa` gets installed too.

```
neplan2pypsa -e elements.edt -n nodes.ndt --csv-dir path/for/csv/files/

```


See also `neplan2pypsa --help`.