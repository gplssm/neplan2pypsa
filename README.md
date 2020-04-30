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

## License

MIT License

Copyright (c) 2020 gplssm

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 