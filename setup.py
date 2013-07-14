
from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = 'pyubertooth',
    version = '0.1',
    description = 'Pure Python Library for Ubertooth',
    author='hackgnar',
    packages = find_packages(),
    long_description = open(join(dirname(__file__), 'README.md')).read(),
    scripts = ['tools/ubertooth_dump.py', 'pyubertooth/ubertooth.py'],
    install_requires = [
        'pyusb'
    ],
    package_data = {
        'pyubertooth': []
    }
)
