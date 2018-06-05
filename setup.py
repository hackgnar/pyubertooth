import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyubertooth',
    version='0.1',
    author='Ryan Holeman',
    description='Pure Python Library for Ubertooth',
    maintainer='Haim Daniel',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hackgnar/pyubertooth',
    packages=setuptools.find_packages(),
    scripts=[
        'bin/pyubertooth_dump',
        'bin/pyubertooth_rx'
    ],
    install_requires=[
        'pyusb',
    ],
    package_data={
        'pyubertooth': []
    }
)
