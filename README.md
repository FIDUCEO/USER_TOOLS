<img alt="FIDUCEO FCDR Tools" align="right" src="http://www.fiduceo.eu/sites/default/files/FIDUCEO-logo.png" />

# User Tools
Public tools to be used with FIDUCEO FCDR and CDR data

## Status
[![Build Status](https://travis-ci.org/FIDUCEO/USER_TOOLS.svg?branch=master)](https://travis-ci.org/FIDUCEO/USER_TOOLS)
[![codecov.io](https://codecov.io/gh/FIDUCEO/USER_TOOLS/branch/master/graphs/badge.svg?)](https://codecov.io/gh/FIDUCEO/USER_TOOLS/branch/master/graphs/badge.svg?)

## Dependencies

The Fiduceo User Tools depend on a number of packages, namely:

* `xarray`
* `netcdf4`
* `numpy`
* `numexpr`
* `dask`


## Installation

Create Python environment that satisfies the package list above. Then

    $ python3 setup.py install

Developers may wish to not install actual Python files into the environment
but instead just create links into their sources:

    $ python3 setup.py develop
    
## Usage
    
After successful installation, the following command-line scripts are available

### fiduceo-radprop

Try 
    
    $ fiduceo-radprop --help


## Customisation

In case you want to extend/customize the FIDUCEO tools, your can provide your own 
code contribution and install it into the Python environment with the installed `fiduceo` 
package.

Here are the steps to your first plugin:

(1) Create a simple Python project `my_project` with the following structure:

    my_project/
        setup.py
        my_package/
            __init__.py
            my_plugin.py
      

(2) In the module `my_plugin.py` define a function `run()` which could be implemented like so:
 
```python 
def run():
    # TODO: add useful example, e.g. register a new algorithm or replace an existing one
    pass 
```
        
(3) The package's `__init__.py` may be left empty.

(4) Write the `setup.py` script using the following template:

```python
from distutils.core import setup

setup(name='my_package',
      version="1.0",
      description='My FIDUCEO tools contrib',
      author='Me',
      packages=['my_package'],
      install_requires=['fiduceo'],
      entry_points={
          'fiduceo_user_tools_plugins': [
              #
              # The following internal plugins are for unit-testing only:
              #
              # _test_plugin_1 does nothing
              'my_plugin = my_package.my_plugin:run_plugin',
          ],
      })  
```

(5) Cd into your project `my_project` and install your contribution module:

    $ cd my_project
    $ python3 setup.py develop
    
The next time you run any FIDUCEO tool, your plugins are executed as well.     

