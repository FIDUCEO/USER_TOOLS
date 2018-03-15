from distutils.core import setup

from setuptools import find_packages

# Get package __version__.
# Same effect as "from fiduceo.tool import __version__",
# but avoids importing the module which may not be installed yet:
__version__ = None
with open('fiduceo/tool/version.py') as f:
    exec(f.read())

setup(name='fiduceo_user_tools',
      version=__version__,
      description='FIDUCEO supporting tools',
      author='Tom Block',
      author_email='tom.block@brockmann-consult.de',
      url='http://www.fiduceo.eu',
      packages=find_packages(),
      install_requires=['numpy>=1.11.0', 'xarray>=0.8.2', 'netcdf4>=1.2.4', 'dask>=0.15.2', 'tensorflow>=1.6'],
      entry_points={
          'console_scripts': [
              'fiduceo-radprop = fiduceo.tool.radprop.cli.main:main',
          ],
          'fiduceo_user_tools_plugins': [
              #
              # The following internal plugins are for unit-testing only:
              #
              # _test_plugin_1 does nothing
              'test1 = fiduceo.tool.plugin:test_plugin_1',
              # _test_plugin_2 raises
              'test2 = fiduceo.tool.plugin:test_plugin_2',
              # _test_plugin_3 does not exist
              'test3 = fiduceo.tool.plugin:test_plugin_3',
          ],
      })
