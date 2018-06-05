from os import path as osp

import setuptools

setuptools.setup(
    name='pyubertooth',
    version='0.1',
    description='Pure Python Library for Ubertooth',
    author='hackgnar',
    packages=setuptools.find_packages(),
    long_description=open(osp.join(osp.dirname(__file__), 'README.md')).read(),
    scripts=['tools/ubertooth_dump.py', 'pyubertooth/ubertooth.py'],
    install_requires=[
        'pyusb'
    ],
    package_data={
        'pyubertooth': []
    }
)
