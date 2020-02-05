# neplan2pypsa

Convert NEPLAN grid data (.edt and .ndt) to [eDisGo](https://edisgo.readthedocs.io/en/dev/)-flavored 
[PyPSA](http://www.pypsa.org/doc/index.html) format.

## Installation

You can install it locally for developing with

    python setup.py install
    

## Code linting

In this template, 3 possible linters are proposed:
- flake8 only sends warnings and error about linting (PEP8)
- pylint sends warnings and error about linting (PEP8) and also allows warning about imports order
- black sends warning but can also fix the files for you

You can perfectly use the 3 of them or subset, at your preference. Don't forget to edit `.travis.yml` if you want to desactivate the automatic testing of some linters!
